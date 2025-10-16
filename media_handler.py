from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import os

MAIN_GROUP_ID = int(os.getenv("MAIN_GROUP_ID"))
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID"))

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photos, videos, documents, and links."""
    if update.effective_chat.id != MAIN_GROUP_ID:
        return

    user = update.effective_user
    message = update.message

    if not message:
        return

    # Detect media or links
    if message.photo or message.video or message.document or message.text and ("http" in message.text or "www" in message.text):
        # Send media/text to admin group
        forwarded = await message.forward(chat_id=ADMIN_GROUP_ID)

        # Notify user in main group
        await message.reply_text("⏳ Waiting for admin approval...")

        # Store metadata (optional)
        context.chat_data[forwarded.message_id] = {
            "user_id": user.id,
            "message_id": message.message_id,
        }

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admins approve media."""
    if update.effective_chat.id != ADMIN_GROUP_ID:
        return

    reply = update.message.reply_to_message
    if not reply:
        await update.message.reply_text("Reply to a media or message to approve.")
        return

    data = context.chat_data.get(reply.message_id)
    if not data:
        await update.message.reply_text("No pending approval found.")
        return

    user_id = data["user_id"]
    await context.bot.send_message(
        chat_id=MAIN_GROUP_ID,
        text=f"✅ Approved by admin: {update.effective_user.first_name}",
        reply_to_message_id=data["message_id"],
    )

async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admins reject media."""
    if update.effective_chat.id != ADMIN_GROUP_ID:
        return

    reply = update.message.reply_to_message
    if not reply:
        await update.message.reply_text("Reply to a media or message to reject.")
        return

    data = context.chat_data.get(reply.message_id)
    if not data:
        await update.message.reply_text("No pending approval found.")
        return

    user_id = data["user_id"]
    await context.bot.send_message(
        chat_id=MAIN_GROUP_ID,
        text=f"❌ Rejected by admin: {update.effective_user.first_name}",
        reply_to_message_id=data["message_id"],
    )

def register_media_handlers(app: Application):
    """Register message handlers for media."""
    app.add_handler(
        MessageHandler(
            filters.Chat(MAIN_GROUP_ID)
            & (filters.PHOTO | filters.VIDEO | filters.Document.ALL | filters.TEXT),
            handle_media,
        )
    )
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("reject", reject))
