import yfinance as yf
import pandas as pd
import numpy as np

# Ticker PT Gudang Garam Tbk (IDX)
ticker = "GGRM.JK"

# Download data historis
try:
    data = yf.download(ticker, start="2023-01-01", end="2025-10-01")  # sesuaikan tanggal
    print(data.head())
    
    # Simpan sebagai CSV
    data.to_csv("GGRM_data.csv")
    print("Data berhasil disimpan di GGRM_data.csv")
except Exception as e:
    print(f"Failed to get ticker '{ticker}' reason:", e)
