import os

# Lokasi file .gitignore
gitignore_path = ".gitignore"

# Template isi .gitignore
gitignore_content = """# -----------------------------
# Flutter / Dart
# -----------------------------
build/
.dart_tool/
.flutter-plugins
.flutter-plugins-dependencies
.packages
.pub-cache/
.pub/
.idea/
*.iml
*.lock
*.log
*.tmp

# Android
*.apk
*.aab
*.gradle
local.properties

# iOS
*.xcworkspace
*.xcuserdatad
Pods/

# -----------------------------
# Python / Flask Backend
# -----------------------------
# Virtual environments
venv/
ENV/
env/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd

# Logs & temporary files
*.log
*.tmp
*.bak

# Databases
*.sqlite3
*.db

# -----------------------------
# Model & Dataset (Large files)
# -----------------------------
*.h5
*.keras
*.pkl
*.ckpt
*.csv
*.npz
*.npy

# Keep only the latest model for Railway
!backend/stock_model.keras

# -----------------------------
# System / IDE
# -----------------------------
.vscode/
.idea/
.DS_Store
Thumbs.db

# -----------------------------
# Railway / Deployment
# -----------------------------
!Procfile
!requirements.txt
!runtime.txt
!Backend.py
!train_realtime.py
"""

# Buat / update file .gitignore
with open(gitignore_path, "w") as f:
    f.write(gitignore_content)

print("✅ File .gitignore berhasil dibuat/diperbarui!")

# Jika belum ada folder backend, buat
if not os.path.exists("backend"):
    os.makedirs("backend")
    print("📁 Folder 'backend' dibuat.")

# Pastikan model placeholder ada
model_path = "backend/stock_model.keras"
if not os.path.exists(model_path):
    with open(model_path, "w") as f:
        f.write("")  # placeholder kosong
    print("🧠 File model placeholder dibuat: backend/stock_model.keras")

print("🚀 Semua konfigurasi Git & model siap untuk Railway Deployment!")
