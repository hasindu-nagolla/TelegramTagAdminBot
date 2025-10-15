import os
import re
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def mention_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:           # Safeguard in case update contains no message
        return
    chat_id = update.effective_chat.id
    message_text = update.message.text
    sender = update.effective_user.mention_html()
    admins = await context.bot.getChatAdministrators(chat_id)
    mentions = []
    for admin in admins:
        user = admin.user
        if user.username:
            mentions.append(f'@{user.username}')
        else:
            mentions.append(user.first_name)
    admin_mentions = ", ".join(mentions)
    # Reply with user's original message and admin mentions
    reply = (
        f"<b>{message_text}</b>\n"
        f"{admin_mentions}"
    )
    await update.message.reply_html(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    # Handles /admin
    admin_handler = CommandHandler("admin", mention_admins)
    # Handles .admin, @admin, /admin, case-insensitive
    regex_handler = MessageHandler(
        filters.Regex(r"(?i)(\.|@|\/)admin"), 
        mention_admins
    )
    app.add_handler(admin_handler)
    app.add_handler(regex_handler)
    app.run_polling()
