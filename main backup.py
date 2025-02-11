from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('kasir.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM barang")
    barang = cursor.fetchall()
    conn.close()
    return render_template('index.html', barang=barang)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM barang WHERE id LIKE ? OR nama LIKE ?", ('%' + query + '%', '%' + query + '%'))
    barang = cursor.fetchall()
    conn.close()
    return render_template('index.html', barang=barang, query=query)

@app.route('/scan_qr')
def scan_qr():
    return render_template('scan_qr.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

