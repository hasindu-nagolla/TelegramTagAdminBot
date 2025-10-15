import os
import re
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def mention_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    admins = await context.bot.getChatAdministrators(chat_id)
    mentions = []
    for admin in admins:
        user = admin.user
        if user.username:
            mentions.append(f'@{user.username}')
        else:
            mentions.append(user.first_name)
    message = "🔔 Calling admins: " + " ".join(mentions)
    await context.bot.send_message(chat_id=chat_id, text=message)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    # Command: /admin
    admin_handler = CommandHandler("admin", mention_admins)
    # Regex: matches '.admin', '@admin', '/admin' anywhere in text (case insensitive)
    regex_handler = MessageHandler(
        filters.Regex(r"(?i)(\.|@|\/)admin")
        mention_admins
    )
    app.add_handler(admin_handler)
    app.add_handler(regex_handler)
    app.run_polling()
