import telebot
from telebot import types
import os

TOKEN = "8726822525:AAE9C5egUSQF8jaDHVeaD4s5SR0nKLX6A1M"

bot = telebot.TeleBot(TOKEN)

user_files = {}

# =========================
# HANDLE FILE (VIDEO / AUDIO)
# =========================
@bot.message_handler(content_types=['video', 'audio'])
def handle_file(message):
    file_id = None
    file_type = None

    if message.content_type == 'video':
        file_id = message.video.file_id
        file_type = "video"
    elif message.content_type == 'audio':
        file_id = message.audio.file_id
        file_type = "audio"

    # ambil file dari telegram
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # ambil ekstensi asli
    ext = file_info.file_path.split('.')[-1]

    # folder aman (penting untuk Railway)
    os.makedirs("files", exist_ok=True)

    input_path = f"files/input_{message.chat.id}.{ext}"

    # simpan file
    with open(input_path, 'wb') as f:
        f.write(downloaded_file)

    user_files[message.chat.id] = input_path

    # tombol
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton("🎥 Video Note", callback_data="vn")
    btn2 = types.InlineKeyboardButton("🎤 Voice Note", callback_data="voice")

    markup.add(btn1, btn2)

    # hanya muncul kalau video
    if file_type == "video":
        btn3 = types.InlineKeyboardButton("🎵 MP3", callback_data="mp3")
        markup.add(btn3)

    bot.send_message(message.chat.id, "Pilih format konversi:", reply_markup=markup)


# =========================
# CALLBACK BUTTON
# =========================
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id
    input_path = user_files.get(chat_id)

    # CEK FILE ADA ATAU TIDAK
    if not input_path or not os.path.exists(input_path):
        bot.send_message(chat_id, "❌ File tidak ditemukan atau sudah terhapus.")
        return

    # =========================
    # VIDEO NOTE (LINGKARAN)
    # =========================
    if call.data == "vn":
        output = f"files/output_vn_{chat_id}.mp4"

        cmd = f'ffmpeg -y -i "{input_path}" -vf "crop=min(iw\\,ih):min(iw\\,ih),scale=512:512" -c:v libx264 -preset ultrafast -c:a copy "{output}"'
        os.system(cmd)

        bot.send_video_note(chat_id, open(output, 'rb'))


    # =========================
    # VOICE NOTE (OGG)
    # =========================
    elif call.data == "voice":
        output = f"files/output_voice_{chat_id}.ogg"

        cmd = f'ffmpeg -y -i "{input_path}" -vn -acodec libopus -b:a 64k "{output}"'
        os.system(cmd)

        bot.send_voice(chat_id, open(output, 'rb'))


    # =========================
    # MP3 (HANYA VIDEO)
    # =========================
    elif call.data == "mp3":
        output = f"files/output_audio_{chat_id}.mp3"

        cmd = f'ffmpeg -y -i "{input_path}" -vn -ab 192k "{output}"'
        os.system(cmd)

        bot.send_audio(chat_id, open(output, 'rb'))


# =========================
# RUN BOT
# =========================
bot.polling()
