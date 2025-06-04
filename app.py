from flask import Flask, render_template, request, redirect, session, url_for, flash
from db import get_connection
# from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ganti dengan kunci rahasia yang aman

# ---------------- AUTH ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and user['password'] == password:  # langsung cocokkan password plain text
            session['user_id'] = user['id']
            session['email'] = user['email']
            return redirect(url_for('home'))
        else:
            flash('Login gagal. Email atau password salah.')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']  # Simpan password plain text

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (name, email, password))  # langsung simpan password plain text
        conn.commit()
        flash('Pendaftaran berhasil. Silakan login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------- HOME & BUKU ----------------

@app.route('/')
def home():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return render_template('home.html', books=books)


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    return render_template('book_detail.html', book=book)

# ---------------- CART ----------------

@app.route('/add-to-cart/<int:book_id>')
def add_to_cart(book_id):
    session_id = session.get('session_id')
    if not session_id:
        import uuid
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id

    conn = get_connection()
    cursor = conn.cursor()

    # Cek apakah item sudah ada
    cursor.execute("SELECT * FROM cart_items WHERE session_id = %s AND book_id = %s", (session_id, book_id))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("UPDATE cart_items SET quantity = quantity + 1 WHERE session_id = %s AND book_id = %s", (session_id, book_id))
    else:
        cursor.execute("INSERT INTO cart_items (book_id, quantity, session_id) VALUES (%s, %s, %s)", (book_id, 1, session_id))

    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    session_id = session.get('session_id')
    if not session_id:
        return redirect(url_for('home'))  # Atau tampilkan pesan "Keranjang kosong"

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ci.id AS cart_id, b.*, ci.quantity
        FROM cart_items ci
        JOIN books b ON ci.book_id = b.id
        WHERE ci.session_id = %s
    """, (session_id,))
    items = cursor.fetchall()

    total = sum(item['price'] * item['quantity'] for item in items)

    return render_template('cart.html', items=items, total=total)

@app.route('/remove-from-cart/<int:cart_id>')
def remove_from_cart(cart_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart_items WHERE id = %s", (cart_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('cart'))


# ---------------- CHECKOUT & PAYMENT ----------------

@app.route('/checkout')
def checkout():
    if 'user_id' not in session or 'session_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    session_id = session['session_id']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name, address, phone FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()

    cursor.execute("""
        SELECT b.title, b.price, ci.quantity
        FROM cart_items ci
        JOIN books b ON ci.book_id = b.id
        WHERE ci.session_id = %s
    """, (session_id,))
    cart_items = cursor.fetchall()

    conn.close()

    if not cart_items:
        flash("Keranjang kosong.")
        return redirect(url_for('cart'))

    total = sum(item['price'] * item['quantity'] for item in cart_items)

    return render_template('checkout.html', user=user_data, cart_items=cart_items, total=total)


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    session_id = session.get('session_id')

    if not session_id:
        flash('Session keranjang tidak ditemukan.')
        return redirect(url_for('cart'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name, address, phone FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    if not user_data:
        flash('Data pengguna tidak ditemukan.')
        return redirect(url_for('cart'))

    if request.method == 'POST':
        cursor.execute("""
            SELECT ci.book_id, b.price, ci.quantity
            FROM cart_items ci
            JOIN books b ON ci.book_id = b.id
            WHERE ci.session_id = %s
        """, (session_id,))
        cart_items = cursor.fetchall()

        if not cart_items:
            flash("Keranjang kosong.")
            return redirect(url_for('cart'))

        total_price = sum(item['price'] * item['quantity'] for item in cart_items)

        cursor.execute("""
            INSERT INTO orders (user_id, session_id, total_price, created_at)
            VALUES (%s, %s, %s, NOW())
        """, (user_id, session_id, total_price))
        order_id = cursor.lastrowid

        for item in cart_items:
            cursor.execute("""
                INSERT INTO orders_item (order_id, book_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (order_id, item['book_id'], item['quantity'], item['price']))

        cursor.execute("DELETE FROM cart_items WHERE session_id = %s", (session_id,))
        conn.commit()
        conn.close()

        flash('Pembayaran berhasil. Terima kasih!')
        return redirect(url_for('orders'))

    cursor.execute("""
        SELECT b.title, b.price, ci.quantity
        FROM cart_items ci
        JOIN books b ON ci.book_id = b.id
        WHERE ci.session_id = %s
    """, (session_id,))
    cart_items = cursor.fetchall()
    total = sum(item['price'] * item['quantity'] for item in cart_items)

    return render_template('payment.html', bank_info={
        'bank': 'BCA',
        'account_number': '1234567890',
        'account_name': 'Toko Buku Amanah'
    }, cart_items=cart_items, total=total, user=user_data)

# ---------------- ORDER HISTORY ----------------

@app.route('/orders')
def orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.id, o.status, b.title, b.price
        FROM orders o
        JOIN books b ON o.book_id = b.id
        WHERE o.user_id = %s
    """, (user_id,))
    orders = cursor.fetchall()
    return render_template('order_history.html', orders=orders)

# ---------------- MAIN ----------------

if __name__ == '__main__':
    app.run(debug=True)
