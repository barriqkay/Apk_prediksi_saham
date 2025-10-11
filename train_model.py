import yfinance as yf
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import joblib

# Konfigurasi
TICKER = "GGRM.JK"   # saham Gudang Garam
PERIOD = "5y"
SEQ_LEN = 60
HORIZON = 1

def fetch_and_prepare(ticker=TICKER, period=PERIOD):
    print("Loading data from CSV...")
    try:
        df = pd.read_csv("GGRM_data.csv", index_col=0, parse_dates=True)
    except FileNotFoundError:
        print("CSV not found, downloading...")
        df = yf.download(ticker, period=period, interval="1d")
        if df.empty:
            raise RuntimeError(f"No data returned for {ticker}. Periksa ticker atau koneksi internet.")
        df.to_csv("GGRM_data.csv")

    df = df[['Open','High','Low','Close','Volume']].dropna()

    features = ['Open', 'High', 'Low', 'Close', 'Volume']
    data = df[features].values.astype(float)
    targets = df['Close'].shift(-HORIZON).values.astype(float)

    # Hapus baris dengan target NaN pakai index
    idx = np.where(~np.isnan(targets))[0]
    data = data[idx, :]
    targets = targets[idx]

    print("DEBUG shapes → data:", data.shape, "targets:", targets.shape)

    X, y = [], []
    for i in range(SEQ_LEN, len(data)):
        X.append(data[i-SEQ_LEN:i])
        y.append(targets[i])
    return np.array(X), np.array(y), df

# Ambil data
X, y, df_full = fetch_and_prepare()
print("Data siap untuk training:", X.shape, y.shape)

# Scale data
scaler = MinMaxScaler(feature_range=(0, 1))
# Fit scaler on all data
all_data = X.reshape(-1, X.shape[2])
scaler.fit(all_data)
# Transform sequences
X_scaled = np.array([scaler.transform(seq) for seq in X])
# For y, fit separate scaler or use same, but since predicting Close, use same scaler on Close
y_scaler = MinMaxScaler(feature_range=(0, 1))
y_scaled = y_scaler.fit_transform(y.reshape(-1, 1)).flatten()

# Bangun model LSTM
model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(X_scaled.shape[1], X_scaled.shape[2])),
    Dropout(0.2),
    LSTM(32),
    Dropout(0.2),
    Dense(1)
])

model.compile(optimizer="adam", loss="mse")
print(model.summary())

# Training model
history = model.fit(X_scaled, y_scaled, epochs=10, batch_size=32, validation_split=0.2)

# Simpan model dan scaler
model.save("stock_model.keras")
joblib.dump(scaler, 'stock_scaler.pkl')
joblib.dump(y_scaler, 'y_scaler.pkl')
print("Model dan scaler disimpan.")

