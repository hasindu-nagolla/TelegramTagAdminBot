# import os
# import re
# from dotenv import load_dotenv
# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# load_dotenv()
# BOT_TOKEN = os.getenv("BOT_TOKEN")

# TRIGGER_PATTERN = re.compile(r"(?i)(\.|@|\/)admin")

# async def mention_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if not update.message:
#         return
#     chat_id = update.effective_chat.id
#     message_text = update.message.text
#     # Remove trigger (.admin, @admin, /admin)
#     cleaned_text = TRIGGER_PATTERN.sub("", message_text).strip()
    
#     sender = update.effective_user
#     user_display = f"{sender.first_name}"
#     if sender.username:
#         user_display += f" (@{sender.username})"
    
#     notify_emoji = "🔔"

#     # Attention-styled report
#     reply_msg = (
#         f"<blockquote><b><i>⚠️ A new report has been submitted and requires your review. 📢</i></b></blockquote>\n"
#         f"<blockquote><b><i>\"{cleaned_text}\"</i></b> from {user_display} {notify_emoji}</blockquote>"
#     )
    
#     admins = await context.bot.getChatAdministrators(chat_id)
#     mentions = []
#     for admin in admins:
#         user = admin.user
#         # Skip anonymous admins
#         if admin.is_anonymous:
#             continue
#         if user.username:
#             mentions.append(f'@{user.username}')
#         else:
#             mentions.append(user.first_name)
    
#     if mentions:
#         admin_mentions = ", ".join(mentions)
#         reply_msg += f"\n<blockquote>{admin_mentions}</blockquote>"
#     else:
#         reply_msg += "\n<blockquote>No visible admins found to mention.</blockquote>"
    
#     await update.message.reply_html(reply_msg)

# if __name__ == "__main__":
#     app = ApplicationBuilder().token(BOT_TOKEN).build()
#     admin_handler = CommandHandler("admin", mention_admins)
#     regex_handler = MessageHandler(
#         filters.Regex(r"(?i)(\.|@|\/)admin"),
#         mention_admins
#     )
#     app.add_handler(admin_handler)
#     app.add_handler(regex_handler)
#     app.run_polling()

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
    # Remove trigger phrase (.admin, @admin, /admin) from user's message
    cleaned_text = TRIGGER_PATTERN.sub("", message_text).strip()

    sender = update.effective_user
    user_display = f"{sender.first_name}"
    if sender.username:
        user_display += f" (@{sender.username})"
    notify_emoji = "🔔"

    reply_msg = (
        f"<blockquote><b><i>⚠️ A new report has been submitted and requires your review. 📢</i></b></blockquote>\n"
        f"<blockquote><b><i>\"{cleaned_text}\"</i></b> from {user_display} {notify_emoji}</blockquote>\n"
    )

    # Build the admin ping list (plain text, triggers real Telegram notifications)
    admins = await context.bot.getChatAdministrators(chat_id)
    mentions = []
    for admin in admins:
        if admin.is_anonymous:
            continue
        user = admin.user
        if user.username:
            mentions.append(f'@{user.username}')     # mention with Telegram notification
        else:
            mentions.append(user.first_name)         # fallback if admin no username

    if mentions:
        reply_msg += " ".join(mentions) + "\n"
    else:
        reply_msg += "No visible admins found to mention.\n"

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
