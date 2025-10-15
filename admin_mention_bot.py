import os
import re
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

TRIGGER_PATTERN = re.compile(r"(?i)(\.|@|\/)admin")

async def mention_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    chat_id = update.effective_chat.id
    message_text = update.message.text
    # Remove .admin, @admin, /admin trigger from message
    cleaned_text = TRIGGER_PATTERN.sub("", message_text).strip()
    sender = update.effective_user
    user_display = f"{sender.first_name}"
    if sender.username:
        user_display += f" (@{sender.username})"
    notify_emoji = "🔔"

    reply_msg = (
        f"<blockquote>A new report has been submitted and requires your review. 🚨</blockquote>\n"
        f"<blockquote><b>\"{cleaned_text}\"</b> from {user_display} {notify_emoji}</blockquote>"
    )
    admins = await context.bot.getChatAdministrators(chat_id)
    mentions = []
    for admin in admins:
        user = admin.user
        if user.username:
            mentions.append(f'@{user.username}')
        else:
            mentions.append(user.first_name)
    admin_mentions = ", ".join(mentions)
    reply_msg += f"\n<blockquote>{admin_mentions}</blockquote>"
    await update.message.reply_html(reply_msg)

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
