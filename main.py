from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import os
import json

# 🔑 Token
TOKEN = os.environ.get("8270124659:AAFAyM14A5nfQuUYxfJ16q-DWTmfDzccVWM")
bot = Bot(token=TOKEN)

# 🗂 Chat ID lar saqlanadigan fayl
CHAT_FILE = "chat_ids.json"

# 🗓 Haftalik reja
schedule = {
    "monday": [
        ("19:00", "🎮 Gaming clip post qilish vaqti!\nHashtag: #uzbekgaming #gamereels #explorepage #neongaming")
    ],
    "tuesday": [
        ("21:00", "😂 Meme / fun moment post qilish!\nHashtag: #gamingcommunity #viralreels #uzbekcontent")
    ],
    "wednesday": [
        ("20:00", "📚 Educational gaming tips!\nHashtag: #reelstips #contentcreator #gaminguz")
    ],
    "thursday": [
        ("22:00", "🚗 Mashina kontenti (Nexia 2 neon style)!\nHashtag: #uzbekcars #carsofinstagram #fyp")
    ],
    "friday": [
        ("23:00", "🔥 Main viral reel!\nHashtag: #viralreels #boostyourreel #uzbekgaming")
    ],
    "saturday": [
        ("17:00", "🎨 Creative neon edit!\nHashtag: #neonvibes #trendingreels #gamerlife"),
        ("22:00", "📸 Extra post (screenshot/trailer)!\nHashtag: #gamingreels #uzbekgaming #explorepage")
    ],
    "sunday": [
        ("20:00", "😌 Chill gaming reel!\nHashtag: #facelesscreator #gamingreels #uzbekblogger")
    ]
}

# 📂 Chat ID larni faylga yozib olish
def load_chat_ids():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            return json.load(f)
    return []

def save_chat_ids(chat_ids):
    with open(CHAT_FILE, "w") as f:
        json.dump(chat_ids, f)

# 🔔 Barcha foydalanuvchilarga xabar yuborish
def send_message(text):
    chat_ids = load_chat_ids()
    for chat_id in chat_ids:
        try:
            bot.send_message(chat_id=chat_id, text=text)
        except:
            pass  # agar foydalanuvchi bloklasa, xatoni tashlamaslik uchun

# 🟢 /start komandasi
def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    chat_ids = load_chat_ids()

    if chat_id not in chat_ids:
        chat_ids.append(chat_id)
        save_chat_ids(chat_ids)

    update.message.reply_text("✅ Sen endi kunlik kontent eslatmalarini olasan!")

# 📅 Bugungi reja
def today(update: Update, context: CallbackContext):
    today = datetime.datetime.today().strftime("%A").lower()
    if today in schedule:
        msg = f"📅 Bugungi reja ({today.title()}):\n\n"
        for time_str, task in schedule[today]:
            msg += f"🕒 {time_str} → {task}\n\n"
    else:
        msg = "Bugungi kun uchun reja yo‘q 📭"
    update.message.reply_text(msg)

# 🗓 Jadval
def schedule_jobs():
    scheduler = BackgroundScheduler()
    for day, tasks in schedule.items():
        for time_str, message in tasks:
            hour, minute = map(int, time_str.split(":"))
            scheduler.add_job(
                send_message,
                "cron",
                day_of_week=day[:3],
                hour=hour,
                minute=minute,
                args=[message]
            )
    scheduler.start()

if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("today", today))

    schedule_jobs()
    updater.start_polling()
    updater.idle()
