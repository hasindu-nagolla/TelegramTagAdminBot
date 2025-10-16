from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photos, videos, documents, and links."""
    main_group_id = context.bot_data.get("MAIN_GROUP_ID")
    admin_group_id = context.bot_data.get("ADMIN_GROUP_ID")

    if update.effective_chat.id != main_group_id:
        return

    user = update.effective_user
    message = update.message

    if not message:
        return

    # Detect media or links
    if message.photo or message.video or message.document or (message.text and ("http" in message.text or "www" in message.text)):
        # Send media/text to admin group
        forwarded = await message.forward(chat_id=admin_group_id)

        # Notify user in main group
        await message.reply_text("⏳ Waiting for admin approval...")

        # Store metadata (temporary memory)
        context.chat_data[forwarded.message_id] = {
            "user_id": user.id,
            "message_id": message.message_id,
        }

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admins approve media."""
    admin_group_id = context.bot_data.get("ADMIN_GROUP_ID")
    main_group_id = context.bot_data.get("MAIN_GROUP_ID")

    if update.effective_chat.id != admin_group_id:
        return

    reply = update.message.reply_to_message
    if not reply:
        await update.message.reply_text("Reply to a media or message to approve.")
        return

    data = context.chat_data.get(reply.message_id)
    if not data:
        await update.message.reply_text("No pending approval found.")
        return

    await context.bot.send_message(
        chat_id=main_group_id,
        text=f"✅ Approved by admin: {update.effective_user.first_name}",
        reply_to_message_id=data["message_id"],
    )

async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admins reject media."""
    admin_group_id = context.bot_data.get("ADMIN_GROUP_ID")
    main_group_id = context.bot_data.get("MAIN_GROUP_ID")

    if update.effective_chat.id != admin_group_id:
        return

    reply = update.message.reply_to_message
    if not reply:
        await update.message.reply_text("Reply to a media or message to reject.")
        return

    data = context.chat_data.get(reply.message_id)
    if not data:
        await update.message.reply_text("No pending approval found.")
        return

    await context.bot.send_message(
        chat_id=main_group_id,
        text=f"❌ Rejected by admin: {update.effective_user.first_name}",
        reply_to_message_id=data["message_id"],
    )

def register_media_handlers(app: Application, main_group_id: int, admin_group_id: int):
    """Register message handlers for media."""
    # Save IDs in bot_data for shared access
    app.bot_data["MAIN_GROUP_ID"] = main_group_id
    app.bot_data["ADMIN_GROUP_ID"] = admin_group_id

    app.add_handler(
        MessageHandler(
            filters.Chat(main_group_id)
            & (filters.PHOTO | filters.VIDEO | filters.Document.ALL | filters.TEXT),
            handle_media,
        )
    )
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("reject", reject))
