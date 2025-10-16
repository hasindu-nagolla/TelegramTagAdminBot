import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from media_handler import register_media_handlers

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MAIN_GROUP_ID = int(os.getenv("MAIN_GROUP_ID"))
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID"))

print("🚀 Telegram Tag Admin Bot starting...")
print(f"Main Group ID: {MAIN_GROUP_ID}")
print(f"Admin Group ID: {ADMIN_GROUP_ID}")

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Pass group IDs when registering handlers
register_media_handlers(app, MAIN_GROUP_ID, ADMIN_GROUP_ID)

app.run_polling()
