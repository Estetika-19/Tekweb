from collections import Counter
from db import get_connection

def recommend_books(user_id, top_n=5):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil buku yang sudah dibeli user
    cursor.execute("""
        SELECT b.category, b.id
        FROM orders_item oi
        JOIN orders o ON oi.order_id = o.id
        JOIN books b ON oi.book_id = b.id
        WHERE o.user_id = %s
    """, (user_id,))
    purchased_books = cursor.fetchall()

    if not purchased_books:
        # Kalau belum pernah beli, rekomendasi random / populer
        cursor.execute("SELECT * FROM books LIMIT %s", (top_n,))
        recommendations = cursor.fetchall()
        conn.close()
        return recommendations

    # Hitung kategori yang paling sering dibeli
    categories = [book['category'] for book in purchased_books]
    top_categories = [cat for cat, _ in Counter(categories).most_common(3)]

    purchased_book_ids = {book['id'] for book in purchased_books}

    # Build placeholders untuk categories
    categories_placeholders = ','.join(['%s'] * len(top_categories))

    # Build placeholders untuk purchased_book_ids, tapi cek dulu kosong atau tidak
    if purchased_book_ids:
        ids_placeholders = ','.join(['%s'] * len(purchased_book_ids))
        query = f"""
            SELECT * FROM books
            WHERE category IN ({categories_placeholders})
            AND id NOT IN ({ids_placeholders})
            LIMIT %s
        """
        params = (*top_categories, *purchased_book_ids, top_n)
    else:
        # Jika belum ada buku yang dibeli (jarang terjadi karena sudah dicek di atas), 
        # abaikan filter id NOT IN
        query = f"""
            SELECT * FROM books
            WHERE category IN ({categories_placeholders})
            LIMIT %s
        """
        params = (*top_categories, top_n)

    cursor.execute(query, params)
    recommendations = cursor.fetchall()
    conn.close()
    return recommendations
