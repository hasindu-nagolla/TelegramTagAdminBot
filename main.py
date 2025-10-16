import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from admin_mention import register_handlers

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    register_handlers(app)
    print("🤖 Admin Mention Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
