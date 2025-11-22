# Quick Start Guide

## 🚀 Running the Bot

1. **Ensure your .env file is configured**:
   ```
   BOT_TOKEN=your_bot_token_here
   ```

2. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the bot**:
   ```bash
   python main.py
   ```

4. **You should see**:
   ```
   🤖 Admin Mention Bot is ONLINE ✔️
   ```

## 📝 Usage Example

### Mention Admins:
```
@admin The chat is being spammed, please help!
```
- Mentions all admins
- Anyone can use this
- Must include a message/reason

Alternative triggers:
```
.admin Need help here
/admin Important question
```

## ⚠️ Important Notes

1. **Message Required**: 
   - You cannot use @admin without a message
   - Example: `@admin help` ✅
   - Example: `@admin` alone ❌

2. **Bot Permissions**:
   - The bot does not need to be an admin
   - It can fetch admin list from any group it's a member of

3. **Mentions**:
   - Admins with usernames: @username
   - Admins without usernames: Clickable name links

## 🔧 Troubleshooting

### Bot doesn't respond:
- Check your BOT_TOKEN in .env
- Ensure the bot is in the group
- Try with `/admin` instead

### No message error:
- Always include a message
- Example: `@admin your message here`

## 📊 Features Summary

| Feature | Command | Who Can Use |
|---------|---------|-------------|
| Mention Admins | @admin | Everyone |

## 🎯 Next Steps

1. Add bot to your Telegram group
2. Test @admin command with a message
3. Enjoy simplified admin notifications!

That's it! Simple and effective. 🎉
