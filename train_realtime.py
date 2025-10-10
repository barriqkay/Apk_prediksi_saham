import yfinance as yf
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
import datetime
import os

os.system("python setup_gitignore.py")

print("✅ TensorFlow version:", tf.__version__)

# --- Download data realtime
ticker = "GGRM.JK"
print(f"📡 Mengunduh data {ticker} dari Yahoo Finance...")

try:
    df = yf.download(ticker, start="2020-01-01", end=datetime.date.today().strftime("%Y-%m-%d"))
except Exception as e:
    print("❌ Gagal mengunduh data:", e)
    exit()

if df.empty:
    print("❌ Data kosong, hentikan training.")
    exit()

print(f"✅ Data berhasil diunduh: {len(df)} baris.")

# --- Preprocessing
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1, 1))

prediction_days = 60
x_train, y_train = [], []

for x in range(prediction_days, len(scaled_data)):
    x_train.append(scaled_data[x - prediction_days:x, 0])
    y_train.append(scaled_data[x, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# --- Model
model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(x_train.shape[1], 1)),
    Dropout(0.2),
    LSTM(64, return_sequences=False),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')
print("🚀 Mulai training model...")
model.fit(x_train, y_train, epochs=10, batch_size=32, verbose=1)

# --- Save model
MODEL_PATH = "stock.model.keras"
model.save(MODEL_PATH)
print(f"✅ Model disimpan di {MODEL_PATH}")
