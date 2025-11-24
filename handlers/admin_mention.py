import re
import asyncio
from colorama import init, Fore, Style
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from telegram.error import TimedOut, NetworkError

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
        try:
            await update.message.reply_html(warning_msg)
        except (TimedOut, NetworkError) as e:
            print(Fore.RED + f"[ERROR] Failed to send warning: {str(e)}")
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
            # Use HTML link format to mention users without username
            mentions.append(f"<a href='tg://user?id={user.id}'>{user.first_name}</a>")

    if mentions:
        reply_msg += ", ".join(mentions) + "\n"
    else:
        reply_msg += "No visible human admins found to mention.\n"

    # Send message with retry logic for timeout errors
    max_retries = 3
    for attempt in range(max_retries):
        try:
            await update.message.reply_html(reply_msg)
            break
        except TimedOut:
            if attempt < max_retries - 1:
                print(Fore.YELLOW + f"[TIMEOUT] Retry {attempt + 1}/{max_retries} for chat {chat_id}")
                await asyncio.sleep(1)  # Wait 1 second before retry
            else:
                print(Fore.RED + f"[ERROR] Failed to send message after {max_retries} attempts")
        except NetworkError as e:
            print(Fore.RED + f"[NETWORK_ERROR] {str(e)}")
            break
        except Exception as e:
            print(Fore.RED + f"[ERROR] Unexpected error: {str(e)}")
            break


# === Function to register handlers ===
def register_handlers(app):
    app.add_handler(CommandHandler("admin", mention_admins))
    app.add_handler(MessageHandler(filters.Regex(r"(?i)(\.|@|\/)admin"), mention_admins))
