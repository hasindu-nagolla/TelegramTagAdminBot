import os
import re
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def mention_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    chat_id = update.effective_chat.id
    message_text = update.message.text
    sender = update.effective_user
    # Format username (bold)
    user_display = f"<b>{sender.first_name}</b>"
    if sender.username:
        user_display += f" (@{sender.username})"
    notify_emoji = "🔔"
    admins = await context.bot.getChatAdministrators(chat_id)
    mentions = []
    for admin in admins:
        user = admin.user
        if user.username:
            mentions.append(f'@{user.username}')
        else:
            mentions.append(user.first_name)
    admin_mentions = ", ".join(mentions)
    reply = (
        f"Hello admins, some report has to mention to you\n"
        f"<blockquote>{message_text} from {user_display} {notify_emoji}</blockquote>\n"
        f"<blockquote>{admin_mentions}</blockquote>"
    )
    await update.message.reply_html(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    admin_handler = CommandHandler("admin", mention_admins)
    regex_handler = MessageHandler(
        filters.Regex(r"(?i)(\.|@|\/)admin"),
        mention_admins
    )
    app.add_handler(admin_handler)
    app.add_handler(regex_handler)
    app.run_polling()
