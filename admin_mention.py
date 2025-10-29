import html
import re
from colorama import init, Fore, Style
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

# Initialize colorama for VPS console output colors
init(autoreset=True)

# Pattern to detect admin trigger words
TRIGGER_PATTERN = re.compile(r"(?i)(\.|@|\/)admin")

# === Main mention function ===
async def mention_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    chat_id = update.effective_chat.id
    message_text = update.message.text or ""
    cleaned_text = TRIGGER_PATTERN.sub("", message_text).strip()

    sender = update.effective_user
    sender_name = sender.full_name or sender.first_name or "Unknown user"
    sender_username = sender.username

    # For console display
    user_display_console = sender_name
    if sender_username:
        user_display_console += f" (@{sender_username})"

    # For telegram formatted display
    sender_name_html = html.escape(sender_name)
    user_display = sender_name_html
    if sender_username:
        user_display += f" (@{html.escape(sender_username)})"

    notify_emoji = "🔔"

    # Prevent empty admin calls
    if not cleaned_text:
        warning_msg = (
            f"<blockquote><b>⚠️ Please provide a reason when tagging admins.</b></blockquote>\n"
            f"<blockquote>Example: <b>@admin There's a problem here.</b></blockquote>"
        )
        await update.message.reply_html(warning_msg)
        return

    # Log to VPS console
    print(
        Fore.CYAN + Style.BRIGHT +
        f"[ADMIN ALERT] User: {user_display_console} | Message: \"{cleaned_text}\" | Chat ID: {chat_id}"
    )

    # Escape text
    safe_message = html.escape(cleaned_text)

    # Blockquote (quoted user message)
    reply_msg = (
        f"<blockquote><b><i>\"{safe_message}\"</i></b>\n"
        f"Reported by: {user_display} {notify_emoji}</blockquote>\n"
    )

    # Get human admins & build REAL (@) notification mentions
    admins = await context.bot.getChatAdministrators(chat_id)
    mentions = []

    for admin in admins:
        user = admin.user
        if admin.is_anonymous or user.is_bot:
            continue  # ignore BOT admins and hidden admins

        display_name = user.full_name or user.first_name or "Admin"

        # ✅ This is the key: using user-id mention → triggers REAL notification
        mentions.append(f'<a href="tg://user?id={user.id}">{html.escape(display_name)}</a>')

    # Mentions MUST be outside blockquote for Telegram to notify
    if mentions:
        reply_msg += "⚠️ Attention: " + ", ".join(mentions)
    else:
        reply_msg += "No visible human admins found."

    # Reply directly to the original message to improve visibility
    await update.message.reply_html(reply_msg, reply_to_message_id=update.message.message_id)


# === Register handlers in main bot file ===
def register_handlers(app):
    app.add_handler(CommandHandler("admin", mention_admins))
    app.add_handler(MessageHandler(filters.Regex(r"(?i)(\.|@|\/)admin"), mention_admins))
