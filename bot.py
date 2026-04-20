import telebot
from telebot import types
import os

TOKEN = "8726822525:AAE9C5egUSQF8jaDHVeaD4s5SR0nKLX6A1M"

bot = telebot.TeleBot(TOKEN)

user_files = {}

# ===== HANDLE FILE =====
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

    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    input_path = f"input_{message.chat.id}"
    with open(input_path, 'wb') as f:
        f.write(downloaded_file)

    user_files[message.chat.id] = input_path

    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton("🎥 Video Note", callback_data="vn")
    btn2 = types.InlineKeyboardButton("🎤 Voice Note", callback_data="vnvoice")

    markup.add(btn1, btn2)

    if file_type == "video":
        btn3 = types.InlineKeyboardButton("🎵 MP3", callback_data="mp3")
        markup.add(btn3)

    bot.send_message(message.chat.id, "Pilih format konversi:", reply_markup=markup)


# ===== CALLBACK BUTTON =====
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id
    input_path = user_files.get(chat_id)

    if not input_path:
        bot.send_message(chat_id, "File tidak ditemukan.")
        return

    # VIDEO NOTE (lingkaran)
    if call.data == "vn":
        output = "output_vn.mp4"
        os.system(f"ffmpeg -i {input_path} -vf crop='min(iw,ih)':'min(iw,ih)',scale=512:512 -c:v libx264 -preset ultrafast -c:a copy {output}")
        bot.send_video_note(chat_id, open(output, 'rb'))

    # VOICE NOTE (ogg)
    elif call.data == "vnvoice":
        output = "output_voice.ogg"
        os.system(f"ffmpeg -i {input_path} -vn -acodec libopus -b:a 64k {output}")
        bot.send_voice(chat_id, open(output, 'rb'))

    # MP3 (hanya video)
    elif call.data == "mp3":
        output = "output.mp3"
        os.system(f"ffmpeg -i {input_path} -vn -ab 192k {output}")
        bot.send_audio(chat_id, open(output, 'rb'))

bot.polling()
