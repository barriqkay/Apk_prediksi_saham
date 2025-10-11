from flask import Flask, jsonify
import tensorflow as tf
import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import joblib
import datetime

app = Flask(__name__)

# Load model and scaler
MODEL_PATH = "stock_model.keras"
SCALER_PATH = "stock_scaler.pkl"
Y_SCALER_PATH = "y_scaler.pkl"
model = tf.keras.models.load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
y_scaler = joblib.load(Y_SCALER_PATH)

@app.route('/')
def home():
    return jsonify({"status": "API is running", "model": MODEL_PATH})

@app.route('/predict', methods=['GET'])
def predict():
    ticker = "GGRM.JK"
    df = yf.download(ticker, period="90d", interval="1d")
    if df.empty:
        return jsonify({"error": "No data available"}), 500

    df = df[['Open','High','Low','Close','Volume']].dropna()
    data = df.values.astype(float)

    if len(data) < 60:
        return jsonify({"error": "Not enough data for prediction"}), 500

    # Scale the last 60 sequences
    scaled_data = scaler.transform(data[-60:])
    x_input = scaled_data.reshape(1, 60, 5)

    pred_scaled = model.predict(x_input)
    pred_price = y_scaler.inverse_transform(pred_scaled)[0][0]

    return jsonify({
        "ticker": ticker,
        "predicted_price": float(pred_price),
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
