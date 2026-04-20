import os
import subprocess
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def convert_to_voice(file_path, output_path):
    # convert ke format voice note (OGG OPUS)
    command = [
        "ffmpeg",
        "-i", file_path,
        "-vn",
        "-acodec", "libopus",
        "-b:a", "64k",
        "-ar", "48000",
        "-ac", "1",
        output_path
    ]
    subprocess.run(command, check=True)

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.audio or update.message.video or update.message.document

    if not file:
        await update.message.reply_text("Kirim MP3 atau MP4 ya.")
        return

    new_file = await file.get_file()

    input_path = "input.file"
    output_path = "output.ogg"

    await new_file.download_to_drive(input_path)

    await convert_to_voice(input_path, output_path)

    await update.message.reply_voice(voice=open(output_path, "rb"))

app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.AUDIO | filters.VIDEO | filters.Document.ALL, handle_audio))

app.run_polling()
