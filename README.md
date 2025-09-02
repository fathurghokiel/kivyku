# kivyku
# 📱 Kivyku - APK Builder dengan Buildozer

Project ini menggunakan **Kivy** dan **Google Generative AI** untuk membuat aplikasi Android.  
Untuk mengubah project ini menjadi APK, gunakan **Buildozer**.

---

## 🚀 Persiapan Lingkungan

### 1. Install Dependensi di Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y python3 python3-pip git zip unzip \
    openjdk-17-jdk build-essential \
    python3-venv python3-dev \
    libffi-dev libssl-dev libsqlite3-dev
2. Install Buildozer
pip install buildozer

📦 Build APK

Clone repo:

git clone https://github.com/fathurghokiel/kivyku.git
cd kivyku


Edit file buildozer.spec jika perlu (misalnya ganti nama app, package, izin, dll).

Jalankan perintah build:

buildozer -v android debug


Hasil APK ada di folder:

bin/kivyku-0.1-debug.apk

📲 Install APK ke HP

Jika HP terhubung dengan USB + aktifkan USB Debugging:

buildozer android deploy run


Atau copy file APK dari folder bin/ ke HP lalu install manual.

⚡ Tips

Pertama kali build agak lama karena harus download Android SDK/NDK.

Kalau ada error "requirements tidak ditemukan", cek lagi bagian:

requirements = python3,kivy,requests,google-generativeai


Gunakan buildozer android clean jika ingin reset build.

