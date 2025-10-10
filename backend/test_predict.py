import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import os

# ======= 1. Path Model dan CSV =======
model_path = "model/my_model.h5"  # Ganti jika nama model berbeda
csv_path = r"C:\Users\user\Desktop\APK PREDIKSI SAHAM NEW\stock_app_new\backend\Gudang Garam Stock Price History.csv"

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model tidak ditemukan di {model_path}")

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV tidak ditemukan di {csv_path}")

# ======= 2. Load Model =======
model = load_model(model_path)
print("✅ Model berhasil dimuat.")

# ======= 3. Load CSV =======
data = pd.read_csv(csv_path)

# ======= 4. Cek Kolom =======
# Sesuaikan nama kolom jika berbeda
required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
for col in required_columns:
    if col not in data.columns:
        raise ValueError(f"Kolom '{col}' tidak ada di CSV. Silakan periksa nama kolom CSV Anda.")

print(f"✅ Data berhasil dimuat: {len(data)} baris")

# ======= 5. Preprocessing =======
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data[required_columns].values)

sequence_length = 60  # 60 hari terakhir untuk prediksi
X_test = []

for i in range(sequence_length, len(scaled_data)):
    X_test.append(scaled_data[i-sequence_length:i])

X_test = np.array(X_test)
print(f"✅ Data siap untuk prediksi: {X_test.shape}")

# ======= 6. Prediksi =======
predicted_scaled = model.predict(X_test, verbose=0)

# Mengembalikan ke skala asli (hanya kolom Close)
predicted_prices = scaler.inverse_transform(
    np.concatenate((np.zeros((predicted_scaled.shape[0], 4)), predicted_scaled), axis=1)
)[:, -1]

# ======= 7. Tampilkan Hasil =======
print("\n📈 Prediksi harga GGRM (10 prediksi terakhir):")
for i, price in enumerate(predicted_prices[-10:]):
    print(f"Prediksi ke-{i+1}: Rp {price:.2f}")
