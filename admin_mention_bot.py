import os
import re
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

TRIGGER_PATTERN = re.compile(r"(?i)(\.|@|\/)admin")


# === Handle Inline Button Clicks (Admins only) ===
async def handle_admin_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user = query.from_user
    chat = query.message.chat

    # Get chat admins
    chat_admins = await context.bot.getChatAdministrators(chat.id)
    admin_ids = [admin.user.id for admin in chat_admins if not admin.is_anonymous]

    # Restrict button clicks to admins only
    if user.id not in admin_ids:
        await query.answer("Only admins can use these buttons.", show_alert=True)
        return

    status_map = {
        "handled": "✅ Handled by admin.",
        "investigating": "🕵 Investigating, please wait.",
        "ignored": "❌ Report ignored.",
    }

    await query.answer(f"Status updated: {status_map[data]}")
    await query.edit_message_text(
        text=f"{query.message.text}\n\n<b>Admin Response:</b> {status_map[data]}",
        parse_mode="HTML",
    )


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

    # If user sends only @admin/.admin without a message
    if not cleaned_text:
        warning_msg = (
            f"<blockquote><b>⚠️ You can't mention admins without a reason.</b></blockquote>\n"
            f"<blockquote>Please include a message. Example: <b>@admin your complaint</b></blockquote>"
        )
        await update.message.reply_html(warning_msg)
        return

    # Build main report message (without title block)
    reply_msg = (
        f"<blockquote><b><i>\"{cleaned_text}\"</i></b>\nReported by: {user_display} {notify_emoji}</blockquote>\n\n"
    )

    # Collect real (non-bot, non-anonymous) admins
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

    # Inline buttons for admin actions (restricted to admins)
    keyboard = [
        [
            InlineKeyboardButton("✅ Handled", callback_data="handled"),
            InlineKeyboardButton("🕵 Investigating", callback_data="investigating"),
            InlineKeyboardButton("❌ Ignore", callback_data="ignored"),
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_html(reply_msg, reply_markup=markup)


# === Bot Entry Point ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("admin", mention_admins))
    app.add_handler(MessageHandler(filters.Regex(r"(?i)(\.|@|\/)admin"), mention_admins))
    app.add_handler(CallbackQueryHandler(handle_admin_response))

    app.run_polling()
