from flask import Flask, render_template, request, jsonify
import os
import psycopg2

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('POSTGRES_DB', 'testdb')
DB_USER = os.environ.get('POSTGRES_USER', 'postgres')
DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'postgres')


def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/api/items', methods=['GET', 'POST'])
def items():
    if request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('name')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO items(name) VALUES(%s) RETURNING id;", (name,))
        _id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'id': _id, 'name': name}), 201

    else:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM items;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        items = [{'id': r[0], 'name': r[1]} for r in rows]
        return jsonify(items)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
