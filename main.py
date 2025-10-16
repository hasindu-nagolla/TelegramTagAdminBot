import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from admin_mention import register_handlers
from colorama import Fore, Style

# Load environment file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    if not BOT_TOKEN:
        print(Fore.RED + Style.BRIGHT + "❌ BOT_TOKEN not set in .env. Please configure it!")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    register_handlers(app)

    print(Fore.YELLOW + Style.BRIGHT + "🤖 Admin Mention Bot is online and running...")
    app.run_polling()

if __name__ == "__main__":
    main()
