import os
import sys
import time
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from telegram.error import TimedOut, NetworkError
from handlers import admin_mention, start_command
from colorama import Fore, Style

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def error_handler(update, context):
    """Global error handler for the bot"""
    error = context.error
    
    if isinstance(error, TimedOut):
        print(Fore.YELLOW + Style.BRIGHT + f"[TIMEOUT] Request timed out: {error}")
    elif isinstance(error, NetworkError):
        print(Fore.RED + Style.BRIGHT + f"[NETWORK_ERROR] Network error occurred: {error}")
    else:
        print(Fore.RED + Style.BRIGHT + f"[ERROR] Unexpected error: {error}")
        import traceback
        traceback.print_exc()


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

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .read_timeout(30)  # Increase read timeout to 30 seconds
        .write_timeout(30)  # Increase write timeout to 30 seconds
        .connect_timeout(30)  # Increase connect timeout to 30 seconds
        .pool_timeout(30)  # Increase pool timeout to 30 seconds
        .build()
    )
    
    # Add global error handler
    app.add_error_handler(error_handler)
    
    # Register start command handler
    start_command.register_handlers(app)
    
    # Register admin mention handler
    admin_mention.register_handlers(app)

    print_animated_status()
    app.run_polling()


if __name__ == "__main__":
    main()
