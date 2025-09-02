[app]

# Nama aplikasi kamu
title = Kivyku
package.name = kivyku
package.domain = org.fathur

# File utama
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# File utama (Python entry point)
main.py = main.py

# Versi aplikasi
version = 0.1

# Requirement Python & lib tambahan
requirements = python3,kivy,requests,google-generativeai

# Orientasi layar (landscape/portrait/sensor)
orientation = portrait

# Izin Android
android.permissions = INTERNET

# Ikon aplikasi (opsional, bisa pakai PNG sendiri)
icon.filename = %(source.dir)s/data/icon.png

# Opsi tambahan
fullscreen = 0


[buildozer]

# Platform build
log_level = 2
warn_on_root = 1

# Gunakan NDK & SDK default
android.api = 33
android.minapi = 21
android.ndk = 25b

# Mode debug dulu (biar gampang install)
build_type = debug

# Jalur ke output
bin.dir = bin
