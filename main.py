import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from admin_mention import register_admin_handlers
from media_handler import register_media_handlers

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
MAIN_GROUP_ID = os.getenv("MAIN_GROUP_ID")
ADMIN_GROUP_ID = os.getenv("ADMIN_GROUP_ID")

if not BOT_TOKEN or not MAIN_GROUP_ID or not ADMIN_GROUP_ID:
    raise ValueError("❌ Missing BOT_TOKEN, MAIN_GROUP_ID, or ADMIN_GROUP_ID in .env file.")

if __name__ == "__main__":
    print("🚀 Telegram Tag Admin Bot starting...")
    print(f"Main Group ID: {MAIN_GROUP_ID}")
    print(f"Admin Group ID: {ADMIN_GROUP_ID}")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register in correct order
    register_media_handlers(app)
    register_admin_handlers(app)

    print("✅ Handlers registered successfully. Polling for updates...")
    app.run_polling()
