import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from media_handler import register_media_handlers

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MAIN_GROUP_ID = os.getenv("MAIN_GROUP_ID")
ADMIN_GROUP_ID = os.getenv("ADMIN_GROUP_ID")

print("🚀 Telegram Tag Admin Bot starting...")
print(f"Main Group ID: {MAIN_GROUP_ID}")
print(f"Admin Group ID: {ADMIN_GROUP_ID}")

app = ApplicationBuilder().token(BOT_TOKEN).build()

register_media_handlers(app)

app.run_polling()
