import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from telegram.error import TimedOut, NetworkError
from colorama import Fore, Style


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with bot information, image, and inline buttons"""
    
    user = update.effective_user
    
    # Welcome message with bot information
    welcome_text = (
        f"👋 <b>Hello {user.first_name}!</b>\n\n"
        f"🤖 <b>Admin Mention Bot</b>\n\n"
        f"I'm here to help you quickly notify all administrators in your group!\n\n"
        f"<b>📋 What I Can Do:</b>\n"
        f"• Mention all group admins with a single command\n"
        f"• Support multiple trigger formats: @admin, .admin, /admin\n"
        f"• Create clickable mentions for all admins (even without usernames)\n"
        f"• Prevent empty notifications - you must include a reason\n\n"
        f"<b>🎯 How to Use:</b>\n"
        f"Simply type <code>@admin</code>, <code>.admin</code>, or <code>/admin</code> followed by your message:\n\n"
        f"<i>Example:</i> <code>@admin We need help with the event!</code>\n\n"
        f"<b>✨ Features:</b>\n"
        f"• Works in any group where I'm added\n"
        f"• Filters out bots and anonymous admins\n"
        f"• Clean, formatted notifications\n"
        f"• No spam - requires a message with each mention\n\n"
        f"Add me to your group and try it out! 🚀"
    )
    
    # Inline keyboard buttons
    keyboard = [
        [
            InlineKeyboardButton("➕ Add to Group", url="https://t.me/AtzioBot?startgroup=true"),
            InlineKeyboardButton("🌐 Website", url="https://atziobot.hasindunagolla.live/")
        ],
        [
            InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/lakzexe"),
            InlineKeyboardButton("⭐ GitHub", url="https://github.com/hasindu-nagolla/telegram-admin-mention-bot")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Log the start command
    print(
        Fore.GREEN + Style.BRIGHT +
        f"[START_COMMAND] User: {user.first_name} (@{user.username or 'no_username'}) | ID: {user.id}"
    )
    
    # Send text message with inline buttons (no image) with retry logic
    max_retries = 3
    for attempt in range(max_retries):
        try:
            await update.message.reply_html(
                welcome_text,
                reply_markup=reply_markup
            )
            break
        except TimedOut:
            if attempt < max_retries - 1:
                print(Fore.YELLOW + f"[TIMEOUT] Retry {attempt + 1}/{max_retries} for start command")
                await asyncio.sleep(1)
            else:
                print(Fore.RED + f"[ERROR] Failed to send start message after {max_retries} attempts")
        except Exception as e:
            print(Fore.RED + f"[ERROR] Failed to send start message: {str(e)}")
            break


async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle help button callback"""
    query = update.callback_query
    await query.answer()
    
    help_text = (
        "<b>📚 How to Use Admin Mention Bot</b>\n\n"
        "<b>Step 1:</b> Add me to your group\n"
        "<b>Step 2:</b> Make sure I have necessary permissions\n"
        "<b>Step 3:</b> Use one of these commands:\n\n"
        "• <code>@admin your message</code>\n"
        "• <code>.admin your message</code>\n"
        "• <code>/admin your message</code>\n\n"
        "<b>Example:</b>\n"
        "<code>@admin We have a spam problem, please check!</code>\n\n"
        "<b>⚠️ Important:</b>\n"
        "You must include a message after the command. Empty mentions are not allowed!\n\n"
        "<b>💡 Tips:</b>\n"
        "• Works with any admin trigger format\n"
        "• All admins (except bots) will be mentioned\n"
        "• Users without usernames will get clickable mentions\n\n"
        "Need more help? Contact the developer!"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")],
        [InlineKeyboardButton("👨‍💻 Contact Developer", url="https://t.me/lakzexe")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_caption(
        caption=help_text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )


async def back_to_start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle back button callback"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    
    welcome_text = (
        f"👋 <b>Hello {user.first_name}!</b>\n\n"
        f"🤖 <b>Admin Mention Bot</b>\n\n"
        f"I'm here to help you quickly notify all administrators in your group!\n\n"
        f"<b>📋 What I Can Do:</b>\n"
        f"• Mention all group admins with a single command\n"
        f"• Support multiple trigger formats: @admin, .admin, /admin\n"
        f"• Create clickable mentions for all admins (even without usernames)\n"
        f"• Prevent empty notifications - you must include a reason\n\n"
        f"<b>🎯 How to Use:</b>\n"
        f"Simply type <code>@admin</code>, <code>.admin</code>, or <code>/admin</code> followed by your message:\n\n"
        f"<i>Example:</i> <code>@admin We need help with the event!</code>\n\n"
        f"<b>✨ Features:</b>\n"
        f"• Works in any group where I'm added\n"
        f"• Filters out bots and anonymous admins\n"
        f"• Clean, formatted notifications\n"
        f"• No spam - requires a message with each mention\n\n"
        f"Add me to your group and try it out! 🚀"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("➕ Add to Group", url="https://t.me/AtzioBot?startgroup=true"),
            InlineKeyboardButton("🌐 Website", url="https://atziobot.hasindunagolla.live/")
        ],
        [
            InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/lakzexe"),
            InlineKeyboardButton("⭐ GitHub", url="https://github.com/hasindu-nagolla/telegram-admin-mention-bot")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_caption(
        caption=welcome_text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )


def register_handlers(app):
    """Register start command and callback handlers"""
    from telegram.ext import CallbackQueryHandler
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(help_callback, pattern="^help$"))
    app.add_handler(CallbackQueryHandler(back_to_start_callback, pattern="^back_to_start$"))
