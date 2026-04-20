import os
import subprocess
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

# ====== START ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kirim MP3 atau MP4 ke saya.")

# ====== HANDLE MP3 ======
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.audio.get_file()
    input_path = "audio.mp3"
    output_path = "voice.ogg"

    await file.download_to_drive(input_path)

    # convert ke voice note (opus)
    subprocess.call([
        "ffmpeg", "-i", input_path,
        "-c:a", "libopus",
        "-b:a", "64k",
        "-vbr", "on",
        output_path
    ])

    await update.message.reply_voice(voice=open(output_path, "rb"))

# ====== HANDLE VIDEO ======
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.video.get_file()
    input_path = "video.mp4"

    await file.download_to_drive(input_path)

    keyboard = [
        [
            InlineKeyboardButton("🎬 Video Note", callback_data="video_note"),
            InlineKeyboardButton("🎵 MP3", callback_data="mp3_from_video"),
        ]
    ]

    await update.message.reply_text(
        "Pilih format convert:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ====== BUTTON ACTION ======
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    input_path = "video.mp4"

    if query.data == "video_note":
        output_path = "circle.mp4"

        subprocess.call([
            "ffmpeg", "-i", input_path,
            "-vf", "crop='min(in_w,in_h)':'min(in_w,in_h)'",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "30",
            "-c:a", "aac",
            output_path
        ])

        await query.message.reply_video_note(video_note=open(output_path, "rb"))

    elif query.data == "mp3_from_video":
        output_path = "audio.mp3"

        subprocess.call([
            "ffmpeg", "-i", input_path,
            "-q:a", "2",
            "-map", "a",
            output_path
        ])

        await query.message.reply_audio(audio=open(output_path, "rb"))

# ====== MAIN ======
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
app.add_handler(MessageHandler(filters.VIDEO, handle_video))

app.add_handler(CallbackQueryHandler(button))

app.run_polling()
