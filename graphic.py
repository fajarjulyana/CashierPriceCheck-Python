from flask import Flask, render_template
import sqlite3
import pandas as pd
import plotly.express as px

app = Flask(__name__)

def get_data():
    conn = sqlite3.connect('database.db')
    query = '''
    SELECT t.tanggal, d.id_barang, d.harga 
    FROM transaksi_log t
    JOIN detail_transaksi d ON t.id = d.transaksi_id
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

@app.route('/')
def index():
    df = get_data()
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    df = df.sort_values(by=['tanggal'])
    
    fig = px.line(df, x='tanggal', y='harga', color='id_barang',
                  title='Grafik Kenaikan Harga', markers=True,
                  animation_frame=df['tanggal'].dt.strftime('%Y-%m-%d'))
    
    graph_html = fig.to_html(full_html=False)
    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
