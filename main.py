import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

# O'zingizning ma'lumotlaringizni yozing:
API_ID = 1234567       # my.telegram.org dan olingan id
API_HASH = "sizning_api_hash"
BOT_TOKEN = "9030184112:AAHiKx2_AR0V9K48TcwKrCplnuR3kJQQ27g"

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Salom! Menga YouTube yoki boshqa sayt havolasini yuboring, uni MP3 musiqa qilib yuklab beraman! 🎧")

@app.on_message(filters.text & ~filters.command("start"))
async def download_music(client, message):
    url = message.text
    if not url.startswith("http"):
        await message.reply_text("Iltimos, to'g'ri havola yuboring!")
        return

    m = await message.reply_text("Musiqa yuklab olinmoqda va MP3 ga o'girilmoqda...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloaded_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        audio_file = "downloaded_audio.mp3"
        await message.reply_audio(audio=audio_file, caption="Mana sizning musiqangiz! 🎵")
        os.remove(audio_file)
        await m.delete()
    except Exception as e:
        await m.edit_text(f"Xatolik yuz berdi: {e}")

app.run()
