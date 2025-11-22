# Telegram Admin Bot

A simple Telegram bot for mentioning all admins in a group with a message.

## Features

### Welcome Message (`/start`)
- Beautiful welcome message with bot information
- Bot logo/image display
- Inline buttons for:
  - Add to Group
  - Help documentation
  - Developer contact
  - GitHub repository
- Interactive help system with navigation

### Mention Admins (`@admin`)
- Any member can mention all admins with a message
- Triggers: `@admin`, `.admin`, or `/admin`
- Requires a message/reason to prevent spam
- Mentions admins with usernames using @username format
- Mentions admins without usernames using clickable mention links
- Example: `@admin Need help with spam messages`

## Project Structure

```
tgadminbot/
├── handlers/              # Message and command handlers
│   ├── __init__.py
│   ├── start_command.py   # /start command with welcome message
│   └── admin_mention.py   # @admin command handler
├── main.py               # Main bot entry point
├── requirements.txt      # Python dependencies
└── sample .env          # Environment variables template
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your bot token:
   ```
   BOT_TOKEN=your_telegram_bot_token_here
   ```

3. Run the bot:
   ```bash
   python main.py
   ```

## Commands

| Command | Access | Description |
|---------|--------|-------------|
| `/start` | All users | Show bot information, features, and help with inline buttons |
| `@admin [message]` | All members | Mention all admins with a message |

## How It Works

1. Any member sends `@admin [message]` (e.g., `@admin Need help`)
2. Bot verifies a message/reason is provided
3. Bot fetches all group administrators
4. Bot mentions all human admins (skips bots and anonymous admins)
5. Admins with usernames: mentioned as @username
6. Admins without usernames: mentioned with clickable name links

## Example Usage

```
User: @admin Someone is spamming the group
Bot: "Someone is spamming the group"
      Reported by: John (@john123) 🔔
      
      @admin1, @admin2, AdminName3, @admin4
```

## Notes

- The bot requires a message with @admin to prevent empty spam mentions
- Only human admins are mentioned (bots and anonymous admins are skipped)
- The bot includes colorized console logging for monitoring

## License

This project is open source and available for modification.
