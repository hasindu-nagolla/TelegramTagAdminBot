import re
from colorama import init, Fore, Style
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

# Initialize colorama for terminal color output
init(autoreset=True)

TRIGGER_PATTERN = re.compile(r"(?i)(\.|@|\/)admin")

# === Main Mention Function ===
async def mention_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    chat_id = update.effective_chat.id
    message_text = update.message.text
    cleaned_text = TRIGGER_PATTERN.sub("", message_text).strip()

    sender = update.effective_user
    user_display = f"{sender.first_name}"
    if sender.username:
        user_display += f" (@{sender.username})"
    notify_emoji = "🔔"

    # Guard condition if user sends empty mentions
    if not cleaned_text:
        warning_msg = (
            f"<blockquote><b>⚠️ You can't mention admins without a reason.</b></blockquote>\n"
            f"<blockquote>Please include a message. Example: <b>@admin your complaint</b></blockquote>"
        )
        await update.message.reply_html(warning_msg)
        return

    # Print VPS-side report in color
    print(
        Fore.CYAN
        + Style.BRIGHT
        + f"[ADMIN_TRIGGER] User: {user_display} | Message: \"{cleaned_text}\" | Chat ID: {chat_id}"
    )

    # Build formatted reply message for Telegram
    reply_msg = (
        f"<blockquote><b><i>\"{cleaned_text}\"</i></b>\nReported by: {user_display} {notify_emoji}</blockquote>\n\n"
    )

    # Filter valid human admins only
    admins = await context.bot.getChatAdministrators(chat_id)
    mentions = []
    for admin in admins:
        user = admin.user
        if admin.is_anonymous or user.is_bot:
            continue
        if user.username:
            mentions.append(f"@{user.username}")
        else:
            mentions.append(user.first_name)

    if mentions:
        reply_msg += ", ".join(mentions) + "\n"
    else:
        reply_msg += "No visible human admins found to mention.\n"

    await update.message.reply_html(reply_msg)


# === Function to register handlers in main.py ===
def register_handlers(app):
    app.add_handler(CommandHandler("admin", mention_admins))
    app.add_handler(MessageHandler(filters.Regex(r"(?i)(\.|@|\/)admin"), mention_admins))
