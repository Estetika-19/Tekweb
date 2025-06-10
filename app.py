from flask import Flask, request, session, jsonify, render_template, flash, redirect
from db import get_connection
from recomendation import recommend_books
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'lokilaufeyson2012'  # For sessions or cookies
app.permanent_session_lifetime = timedelta(days=1)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/recommendations')
def api_recommendations():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    recommended_books = recommend_books(user_id)
    return jsonify(recommended_books)

# --- Helper: get user by email ---
def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# --- Register ---
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    name = data.get('name')
    username = data.get('username')
    phone = data.get('phone')
    email = data.get('email')
    address = data.get('address')
    password = data.get('password')

    if not all([name, username, phone, email, address, password]):
        return jsonify({'error': 'Semua field wajib diisi'}), 400

    if get_user_by_email(email):
        return jsonify({'error': 'Email sudah terdaftar'}), 400

    if get_user_by_username(username):
        return jsonify({'error': 'Username sudah digunakan'}), 400

    hashed_password = generate_password_hash(password)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (name, username, phone, email, address, password)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, username, phone, email, address, hashed_password))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Registrasi berhasil!'}), 201

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

# --- Login ---
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not (email and password):
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = get_user_by_email(email)
    if user and check_password_hash(user['password'], password):
        # Use session or generate token here
        session['user_id'] = user['id']
        session['email'] = user['email']
        return jsonify({'message': 'Login successful', 'user_id': user['id'], 'email': user['email']}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            session.permanent = True
            session['user_id'] = user['id']
            session['email'] = user['email']
            return redirect('/')  # arahkan ke home setelah login

        flash('Email atau password salah')
        return redirect('/login')

    return render_template('login.html')

# --- Logout ---
@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'message': 'Logged out'}), 200

# --- List all books ---
@app.route('/api/books', methods=['GET'])
def api_books():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return jsonify(books), 200

# --- Book detail ---
@app.route('/book/<int:book_id>', methods=['GET'])
def page_book_detail(book_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    conn.close()
    
    if book:
        return render_template('book_detail.html', book=book)
    return "Book not found", 404    

@app.route('/api/cart/add', methods=['POST'])
def api_add_to_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']

    try:
        data = request.get_json(force=True)
        book_id = data.get('book_id')
        quantity = int(data.get('quantity', 1))

        if not book_id:
            return jsonify({'error': 'book_id is required'}), 400

        conn = get_connection()
        cursor = conn.cursor()

        # Cek apakah item sudah ada di cart untuk user ini
        cursor.execute("""
            SELECT id, quantity FROM cart_items
            WHERE user_id = %s AND book_id = %s
        """, (user_id, book_id))
        existing = cursor.fetchone()

        if existing:
            # Update quantity jika sudah ada
            new_quantity = existing[1] + quantity
            cursor.execute("""
                UPDATE cart_items SET quantity = %s WHERE id = %s
            """, (new_quantity, existing[0]))
        else:
            # Tambahkan item baru
            cursor.execute("""
                INSERT INTO cart_items (user_id, book_id, quantity)
                VALUES (%s, %s, %s)
            """, (user_id, book_id, quantity))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': f'Added book {book_id} to cart'}), 200

    except Exception as e:
        return jsonify({'error': f'Failed to add to cart: {str(e)}'}), 500

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect('/login')
    
    user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT ci.id as cart_id, b.title, b.image_url, b.price, ci.quantity
        FROM cart_items ci
        JOIN books b ON ci.book_id = b.id
        WHERE ci.user_id = %s
    """, (user_id,))
    cart_items = cursor.fetchall()

    total = sum(item['price'] * item['quantity'] for item in cart_items)

    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/api/cart/remove/<int:cart_id>', methods=['DELETE'])
def api_remove_from_cart(cart_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart_items WHERE id = %s", (cart_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Item removed from cart'}), 200

# --- Checkout ---#

@app.route('/api/checkout')
def api_checkout():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name, address, phone FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    cursor.execute("""
        SELECT ci.id as cart_id, b.title, b.price, b.image_url, ci.quantity
        FROM cart_items ci
        JOIN books b ON ci.book_id = b.id
        WHERE ci.user_id = %s
    """, (user_id,))
    cart_items = cursor.fetchall()

    total = sum(item['price'] * item['quantity'] for item in cart_items)

    cursor.close()
    conn.close()

    return jsonify({
        'user': user,
        'cart_items': cart_items,
        'total': total
    })


@app.route('/checkout', methods=['GET', 'POST'])
def page_checkout():
    user_id = session.get('user_id')
    if not user_id:
        flash('Silakan login terlebih dahulu')
        return redirect('/login')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Ambil isi keranjang user untuk simpan ke order
        cursor.execute("""
            SELECT ci.book_id, b.price, ci.quantity
            FROM cart_items ci
            JOIN books b ON ci.book_id = b.id
            WHERE ci.user_id = %s
        """, (user_id,))
        cart_items = cursor.fetchall()

        if not cart_items:
            flash("Keranjang kosong, tidak bisa checkout")
            conn.close()
            return redirect('/cart')

        total_price = sum(item['price'] * item['quantity'] for item in cart_items)

        # Simpan order baru dengan status pending
        cursor.execute("INSERT INTO orders (user_id, total_price, status) VALUES (%s, %s, %s)",
                       (user_id, total_price, 'Pending'))
        order_id = cursor.lastrowid

        # Simpan order_items
        for item in cart_items:
            cursor.execute(
                "INSERT INTO order_items (order_id, book_id, price, quantity) VALUES (%s, %s, %s, %s)",
                (order_id, item['book_id'], item['price'], item['quantity'])
            )

        # Hapus cart_items user setelah checkout
        cursor.execute("DELETE FROM cart_items WHERE user_id = %s", (user_id,))

        conn.commit()
        conn.close()

        # Redirect ke halaman payment untuk order tersebut
        return redirect(url_for('payment', order_id=order_id))

    else:
        # GET request: tampilkan halaman checkout seperti sebelumnya
        cursor.execute("SELECT name, address, phone FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        cursor.execute("""
            SELECT ci.id as cart_id, b.title, b.price, b.image_url, ci.quantity
            FROM cart_items ci
            JOIN books b ON ci.book_id = b.id
            WHERE ci.user_id = %s
        """, (user_id,))
        cart_items = cursor.fetchall()

        total = sum(item['price'] * item['quantity'] for item in cart_items)

        conn.close()

        return render_template('checkout.html', user=user, items=cart_items, total=total)

# --- Payment ---

@app.route('/payment/<int:order_id>', methods=['GET', 'POST'])
def payment(order_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM orders WHERE id=%s AND user_id=%s", (order_id, user_id))
    order = cursor.fetchone()
    if not order:
        flash("Order tidak ditemukan.")
        return redirect('/')

    cursor.execute("""
        SELECT b.title, oi.price, oi.quantity
        FROM order_items oi
        JOIN books b ON oi.book_id = b.id
        WHERE oi.order_id = %s
    """, (order_id,))
    items = cursor.fetchall()

    bank_info = {
        'bank': 'Bank ABC',
        'account_number': '1234567890',
        'account_name': 'Toko Buku XYZ'
    }

    if request.method == 'POST':
        cursor.execute("UPDATE orders SET status=%s WHERE id=%s", ('Menunggu konfirmasi', order_id))
        conn.commit()
        conn.close()

        flash("Terima kasih! Pembayaran Anda sedang diproses.")
        return redirect('/orders')

    conn.close()
    return render_template('payment.html', order=order, items=items, bank_info=bank_info)

@app.route('/api/payment', methods=['POST'])
def api_payment():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'Cart session not found'}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name, address, phone FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    if not user_data:
        return jsonify({'error': 'User data not found'}), 404

    cursor.execute("""
        SELECT ci.book_id, b.price, ci.quantity
        FROM cart_items ci
        JOIN books b ON ci.book_id = b.id
        WHERE ci.session_id = %s
    """, (session_id,))
    cart_items = cursor.fetchall()

    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400

    total_price = sum(item['price'] * item['quantity'] for item in cart_items)

    cursor.execute("""
        INSERT INTO orders (user_id, session_id, total_price, created_at, status)
        VALUES (%s, %s, %s, NOW(), %s)
    """, (user_id, session_id, total_price, 'paid'))
    order_id = cursor.lastrowid

    for item in cart_items:
        cursor.execute("""
            INSERT INTO orders_item (order_id, book_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, item['book_id'], item['quantity'], item['price']))

    cursor.execute("DELETE FROM cart_items WHERE session_id = %s", (session_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Payment successful', 'order_id': order_id}), 200

@app.route('/payment', methods=['GET', 'POST'])
def page_payment():
    user_id = session.get('user_id')
    if not user_id:
        flash('Silakan login terlebih dahulu')
        return redirect('/login')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil info bank (bisa hardcode atau dari DB)
    bank_info = {
        'bank': 'Bank ABC',
        'account_number': '1234567890',
        'account_name': 'Nama Toko Buku'
    }

    # Ambil isi keranjang user
    cursor.execute("""
        SELECT b.title, b.price, ci.quantity
        FROM cart_items ci
        JOIN books b ON ci.book_id = b.id
        WHERE ci.user_id = %s
    """, (user_id,))
    cart_items = cursor.fetchall()

    total = sum(item['price'] * item['quantity'] for item in cart_items)

    if request.method == 'POST':
        # Simpan order ke DB (proses pembayaran sudah konfirmasi)
        cursor.execute("""
            INSERT INTO orders (user_id, total_price, created_at, status)
            VALUES (%s, %s, NOW(), %s)
        """, (user_id, total, 'paid'))
        order_id = cursor.lastrowid

        for item in cart_items:
            cursor.execute("""
                INSERT INTO orders_item (order_id, book_id, quantity, price)
                SELECT %s, b.id, ci.quantity, b.price
                FROM books b JOIN cart_items ci ON b.id = ci.book_id
                WHERE ci.user_id = %s AND b.title = %s
            """, (order_id, user_id, item['title']))

        # Hapus keranjang setelah bayar
        cursor.execute("DELETE FROM cart_items WHERE user_id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Pembayaran berhasil! Terima kasih.')
        return redirect('/orders')  # atau halaman lain

    cursor.close()
    conn.close()

    return render_template('payment.html', bank_info=bank_info, cart_items=cart_items, total=total)

# --- Order history ---
@app.route('/api/orders', methods=['GET'])
def api_orders():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, total_price, created_at, status
        FROM orders
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))
    order_list = cursor.fetchall()

    orders = []
    for order in order_list:
        if order['total_price'] == 0:
            continue  # skip order dengan total 0

        cursor.execute("""
            SELECT b.title, oi.quantity, oi.price
            FROM orders_item oi
            JOIN books b ON oi.book_id = b.id
            WHERE oi.order_id = %s
        """, (order['id'],))
        items = cursor.fetchall()

        orders.append({
            'id': order['id'],
            'total_price': order['total_price'],
            'created_at': order['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
            'status': order['status'],
            'items': items
        })

    conn.close()
    return jsonify({'orders': orders}), 200

@app.route('/orders')
def page_orders():
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu')
        return redirect('/login')

    return render_template('order_history.html')


if __name__ == '__main__':
    app.run(debug=True)
