from telegram.ext import MessageHandler, CallbackQueryHandler, filters

load_dotenv()

MAIN_GROUP_ID = int(os.getenv("MAIN_GROUP_ID"))
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID"))


# === Forward Media from Main Group to Admin Group ===
async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    chat_id = update.effective_chat.id

    # Only process media from main group
    if chat_id != MAIN_GROUP_ID:
        return

    # Ignore admins’ media
    admins = await context.bot.getChatAdministrators(MAIN_GROUP_ID)
    admin_ids = [a.user.id for a in admins if not a.is_anonymous]
    if message.from_user.id in admin_ids or message.from_user.is_bot:
        return

    # Forward message to admin group
    forwarded = await message.forward(chat_id=ADMIN_GROUP_ID)
    user_id = message.from_user.id
    message_id = message.message_id

    # Add buttons for review
    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve:{user_id}:{message_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject:{user_id}:{message_id}")
        ]
    ]
    await forwarded.reply_text("🧐 Review this submission:", reply_markup=InlineKeyboardMarkup(keyboard))

    # Notify sender
    notice = await message.reply_text("⏳ Your media is awaiting admin approval.")
    await context.job_queue.run_once(delete_notice, 60, data=notice.message_id, chat_id=chat_id)


# === Auto-delete temporary notice ===
async def delete_notice(context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.delete_message(chat_id=context.job.chat_id, message_id=context.job.data)
    except Exception:
        pass


# === Handle Approve / Reject ===
async def handle_media_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split(":")
    action, user_id, message_id = data[0], int(data[1]), int(data[2])

    if action == "approve":
        await query.answer("✅ Approved")
        await forward_to_main_group(context, user_id, message_id)
        await query.edit_message_text("✅ Approved and published in main group.")
    elif action == "reject":
        await query.answer("❌ Rejected")
        await query.edit_message_text("❌ Media rejected.")
        await notify_reject(context, user_id)


# === Forward Approved Media Back to Main Group ===
async def forward_to_main_group(context: ContextTypes.DEFAULT_TYPE, user_id: int, message_id: int):
    try:
        await context.bot.forward_message(chat_id=MAIN_GROUP_ID, from_chat_id=ADMIN_GROUP_ID, message_id=message_id)
        await context.bot.send_message(chat_id=user_id, text="✅ Your media has been approved and published.")
    except Exception as e:
        print(f"Error forwarding media: {e}")


# === Notify User of Rejection ===
async def notify_reject(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    try:
        await context.bot.send_message(chat_id=user_id, text="❌ Your media was rejected by the admins.")
    except Exception:
        pass


# === Register Handlers ===
def register_media_handlers(app):
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.Document.ALL | filters.Entity("url"), handle_media))
    app.add_handler(CallbackQueryHandler(handle_media_review, pattern="^(approve|reject):"))
