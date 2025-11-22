import os
import sys
import time
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from handlers import admin_mention, start_command
from colorama import Fore, Style

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


def print_animated_status():
    status = "🤖 Admin Mention Bot is online "
    for i in range(5):
        dots = "." * (i % 4)
        sys.stdout.write(Fore.RED + Style.BRIGHT + f"\r{status}{dots}  ")
        sys.stdout.flush()
        time.sleep(0.4)
    print(Fore.RED + Style.BRIGHT + "\r🤖 Admin Mention Bot is ONLINE ✔️      ")


def main():
    if not BOT_TOKEN:
        print(Fore.RED + Style.BRIGHT +
              "❌ BOT_TOKEN not set in .env. Please configure it!")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Register start command handler
    start_command.register_handlers(app)
    
    # Register admin mention handler
    admin_mention.register_handlers(app)

    print_animated_status()
    app.run_polling()


if __name__ == "__main__":
    main()
