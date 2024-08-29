from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.express as px
import plotly.io as pio
import joblib

app = Flask(__name__)

# Load hasil prediksi dan informasi tambahan
forecast_results = pd.read_csv('/workspaces/codespaces-jupyter/notebooks/forecast_results.csv')
additional_info = joblib.load('/workspaces/codespaces-jupyter/models/additional_info.pkl')

# Load model SVR dan scaler
svr = joblib.load('/workspaces/codespaces-jupyter/models/best_svr_model.pkl')
scaler = joblib.load('/workspaces/codespaces-jupyter/models/scaler.pkl')


@app.route('/')
def home():
    # Buat chart Plotly
    fig = px.line(forecast_results, x='Tanggal Harga', y='Harga Beli Pasar per Kilogram', color='Jenis Sayuran',
                  title='Prediksi Harga Sayuran',
                  labels={'Harga Beli Pasar per Kilogram': 'Harga (IDR)', 'Tanggal Harga': 'Tanggal', 'Jenis Sayuran': 'Sayuran'})
    
    # Konversi chart Plotly ke HTML
    graph_html = pio.to_html(fig, full_html=False)
    
    return render_template('index.html', graph_html=graph_html, additional_info=additional_info)

@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    return jsonify(forecast_results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)