import html
import re
from colorama import init, Fore, Style
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from telegram.utils.helpers import mention_html

# Initialize colorama for terminal color output
init(autoreset=True)

TRIGGER_PATTERN = re.compile(r"(?i)(\.|@|\/)admin")

# === Main Mention Function ===
async def mention_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    chat_id = update.effective_chat.id
    message_text = update.message.text or ""
    cleaned_text = TRIGGER_PATTERN.sub("", message_text).strip()

    sender = update.effective_user
    sender_name = sender.full_name or sender.first_name or "Unknown user"
    sender_username = sender.username

    # Display for console logs
    user_display_console = sender_name
    if sender_username:
        user_display_console += f" (@{sender_username})"

    # Telegram-safe display
    sender_name_html = html.escape(sender_name)
    user_display = sender_name_html
    if sender_username:
        user_display += f" (@{html.escape(sender_username)})"

    notify_emoji = "🔔"

    # Guard condition — require a reason/message
    if not cleaned_text:
        warning_msg = (
            f"<blockquote><b>⚠️ You can't mention admins without a reason.</b></blockquote>\n"
            f"<blockquote>Please include a message. Example:<br><b>@admin issue here</b></blockquote>"
        )
        await update.message.reply_html(warning_msg)
        return

    # Console log
    print(
        Fore.CYAN + Style.BRIGHT +
        f"[ADMIN_TRIGGER] User: {user_display_console} | Message: \"{cleaned_text}\" | Chat ID: {chat_id}"
    )

    # Prepare formatted message
    safe_message = html.escape(cleaned_text)
    reply_msg = (
        f"<blockquote><b><i>\"{safe_message}\"</i></b>\n"
        f"Reported by: {user_display} {notify_emoji}</blockquote>\n\n"
    )

    # Get human admins and build REAL mention notifications
    admins = await context.bot.getChatAdministrators(chat_id)
    mentions = []

    for admin in admins:
        user = admin.user

        # Skip anonymous admins & bots
        if admin.is_anonymous or user.is_bot:
            continue

        # ALWAYS Mention using User ID → Triggers REAL notification
        display_name = user.full_name or user.first_name or "Admin"
        mentions.append(f'<a href="tg://user?id={user.id}">{html.escape(display_name)}</a>')
        main

    if mentions:
        reply_msg += ", ".join(mentions) + "\n"
    else:
        reply_msg += "No visible human admins found.\n"

    # Reply to original message (Improves notification delivery)
    await update.message.reply_html(reply_msg, reply_to_message_id=update.message.message_id)


# === Handler Registration ===
def register_handlers(app):
    app.add_handler(CommandHandler("admin", mention_admins))
    app.add_handler(MessageHandler(filters.Regex(r"(?i)(\.|@|\/)admin"), mention_admins))
