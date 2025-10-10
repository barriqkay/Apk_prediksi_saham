from flask import Flask, jsonify
import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import datetime

app = Flask(__name__)

MODEL_PATH = "backend/stock_model.keras"

@app.route('/')
def home():
    return jsonify({"message": "🚀 Flask Stock Predictor is running on Railway!"})

@app.route('/predict', methods=['GET'])
def predict():
    model = load_model(MODEL_PATH)
    ticker = "GGRM.JK"
    df = yf.download(ticker, period="90d", interval="1d")

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(df['Close'].values.reshape(-1, 1))

    x_input = scaled[-60:].reshape(1, 60, 1)
    pred_scaled = model.predict(x_input)
    pred_price = scaler.inverse_transform(pred_scaled)[0][0]

    return jsonify({
        "ticker": ticker,
        "predicted_price": float(pred_price),
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
