import yt_dlp
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 Replace this with your bot token
BOT_TOKEN = "YOUR_BOT_TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a YouTube link and I'll download the audio for you!")

async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("🎶 Downloading audio, please wait...")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloaded_audio.%(ext)s',
            'noplaylist': True,  # ✅ only download one video, not the whole playlist
            'ffmpeg_location': r"PATH_FOR_FFMPEG",  # path to ffmpeg
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }



        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            audio_file = filename.rsplit(".", 1)[0] + ".mp3"

        # Send audio to user
        with open(audio_file, "rb") as f:
            await update.message.reply_audio(f, title=info.get("title", "Audio"))

        # ✅ Delete the file after sending
        if os.path.exists(audio_file):
            os.remove(audio_file)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

