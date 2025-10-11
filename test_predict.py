import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

# ======= 1. Path Model dan Scaler =======
model_path = "stock_model.keras"
scaler_path = "stock_scaler.pkl"
y_scaler_path = "y_scaler.pkl"
csv_path = "GGRM_data.csv"  # Asumsi dari dataGGRM.py

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model tidak ditemukan di {model_path}")

if not os.path.exists(scaler_path):
    raise FileNotFoundError(f"Scaler tidak ditemukan di {scaler_path}")

if not os.path.exists(y_scaler_path):
    raise FileNotFoundError(f"Y Scaler tidak ditemukan di {y_scaler_path}")

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV tidak ditemukan di {csv_path}")

# ======= 2. Load Model dan Scaler =======
model = load_model(model_path)
scaler = joblib.load(scaler_path)
y_scaler = joblib.load(y_scaler_path)
print("✅ Model dan scaler berhasil dimuat.")

# ======= 3. Load CSV =======
data = pd.read_csv(csv_path)

# ======= 4. Cek Kolom =======
required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
for col in required_columns:
    if col not in data.columns:
        raise ValueError(f"Kolom '{col}' tidak ada di CSV. Silakan periksa nama kolom CSV Anda.")

print(f"✅ Data berhasil dimuat: {len(data)} baris")

# ======= 5. Preprocessing =======
scaled_data = scaler.transform(data[required_columns].values)

sequence_length = 60  # 60 hari terakhir untuk prediksi
X_test = []

for i in range(sequence_length, len(scaled_data)):
    X_test.append(scaled_data[i-sequence_length:i])

X_test = np.array(X_test)
print(f"✅ Data siap untuk prediksi: {X_test.shape}")

# ======= 6. Prediksi =======
predicted_scaled = model.predict(X_test, verbose=0)

# Mengembalikan ke skala asli
predicted_prices = y_scaler.inverse_transform(predicted_scaled).flatten()

# ======= 7. Tampilkan Hasil =======
print("\n📈 Prediksi harga GGRM (10 prediksi terakhir):")
for i, price in enumerate(predicted_prices[-10:]):
    print(f"Prediksi ke-{i+1}: Rp {price:.2f}")
