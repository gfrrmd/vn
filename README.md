# 🎬 Video to VN Bot Telegram

Bot Telegram untuk mengkonversi **video** dan **audio** menjadi berbagai format menggunakan `ffmpeg`. Dibangun dengan Python dan `pyTelegramBotAPI`.

---

## ✨ Fitur

- 🎬 **Video → Video Note** — konversi video jadi pesan lingkaran (video note)
- 🎤 **Video/Audio → Voice Note** — konversi ke pesan suara (format `.ogg` opus)
- 🎵 **Video → MP3** — ekstrak audio dari video menjadi file MP3 192kbps
- Pilihan format via tombol inline keyboard
- Mendukung file **video** dan **audio** dari Telegram

---

## ⚠️ Penting: Keamanan Token

Saat ini `TOKEN` di `bot.py` di-hardcode langsung. **Sangat disarankan** untuk menggantinya dengan environment variable agar token tidak ter-expose di GitHub:

```python
# Ganti baris ini di bot.py:
TOKEN = "<token_kamu>"

# Menjadi:
import os
TOKEN = os.getenv("BOT_TOKEN")
```

---

## 🚀 Cara Deploy di Railway

### 1. Fork / Clone Repo ini
```bash
git clone https://github.com/gfrrmd/Video-to-VN-Bot-Telegram.git
cd Video-to-VN-Bot-Telegram
```

### 2. Update bot.py agar pakai Environment Variable
Ganti baris TOKEN di `bot.py` seperti contoh di atas sebelum deploy.

### 3. Buat Project Baru di Railway
1. Buka [railway.app](https://railway.app) dan login
2. Klik **New Project** → **Deploy from GitHub repo**
3. Pilih repo ini

### 4. Set Environment Variables
Di dashboard Railway, buka tab **Variables** dan tambahkan:

| Variable | Keterangan |
|----------|-----------|
| `BOT_TOKEN` | Token bot dari [@BotFather](https://t.me/BotFather) |

### 5. Deploy
Railway akan otomatis build menggunakan **Dockerfile** yang sudah menyertakan instalasi `ffmpeg`. Bot akan langsung berjalan setelah build selesai.

> 💡 Repo ini sudah menyertakan `Dockerfile` dengan `ffmpeg` dan `nixpacks.toml` untuk kompatibilitas Railway.

---

## 🤖 Cara Pakai Bot

1. Start bot (atau langsung kirim file)
2. Kirim **video** atau **audio** ke bot
3. Pilih format yang diinginkan via tombol:
   - **🎬 Video Note** — jadi pesan lingkaran
   - **🎤 Voice Note** — jadi pesan suara
   - **🎵 MP3** — ekstrak audio (khusus video)
4. Bot mengirimkan hasil konversi

---

## 🛠️ Tech Stack

- **Python 3.11**
- **pyTelegramBotAPI (telebot)**
- **FFmpeg** — untuk konversi media
- **Docker** — environment siap pakai
- Deploy via **Railway**

---

## 📁 Struktur File

```
├── bot.py             # Logika utama bot
├── requirements.txt   # Dependensi Python
├── Dockerfile         # Docker build dengan ffmpeg
├── nixpacks.toml      # Konfigurasi nixpacks Railway
├── Procfile           # Konfigurasi proses Railway
└── README.md
```
