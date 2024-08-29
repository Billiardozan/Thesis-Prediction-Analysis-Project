from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.express as px
import plotly.io as pio
import joblib

app = Flask(__name__)

# Load dataset utama
main_dataset = pd.read_csv('data/processed/harga_sayuran_clean.csv')  # Update with the correct path to your main dataset


# Load hasil prediksi dan informasi tambahan
forecast_results = pd.read_csv('/workspaces/codespaces-jupyter/notebooks/forecast_results.csv')
additional_info = joblib.load('/workspaces/codespaces-jupyter/models/additional_info.pkl')

# Load model SVR dan scaler
svr = joblib.load('/workspaces/codespaces-jupyter/models/best_svr_model.pkl')
scaler = joblib.load('/workspaces/codespaces-jupyter/models/scaler.pkl')

# Ambil 6 data terakhir dari tahun 2023
last_price = main_dataset[main_dataset['Tanggal Harga'].str.contains('2023')].tail(6).to_dict(orient='records')


@app.route('/')
def home():
    # Buat chart Plotly
    fig = px.line(forecast_results, x='Tanggal Harga', y='Harga Beli Pasar per Kilogram', color='Jenis Sayuran',
                  title='Prediksi Harga Sayuran',
                  labels={'Harga Beli Pasar per Kilogram': 'Harga (IDR)', 'Tanggal Harga': 'Tanggal', 'Jenis Sayuran': 'Sayuran'},
                  markers=True)
    
    # Konversi chart Plotly ke HTML
    graph_html = pio.to_html(fig, full_html=False)
    
    return render_template  ('index.html', graph_html=graph_html, additional_info=additional_info, last_price=last_price)

@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    return jsonify(forecast_results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)