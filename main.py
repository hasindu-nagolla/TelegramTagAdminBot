import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from admin_mention import register_admin_handlers
from media_handler import register_media_handlers

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    register_admin_handlers(app)
    register_media_handlers(app)
    app.run_polling()
