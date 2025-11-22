# /start Command Guide

## Overview
The `/start` command provides users with a beautiful welcome message that includes:
- Bot information and features
- A welcome image/logo
- Interactive inline buttons
- Help documentation

## What Users See

When users send `/start` to the bot (in private chat), they receive:

### 1. **Welcome Image**
- A custom bot logo/image is displayed at the top

### 2. **Welcome Message**
The message includes:
- Personal greeting with the user's name
- Bot introduction
- List of features and capabilities
- Usage instructions with examples
- Quick tips

### 3. **Inline Buttons**

#### First Row:
- **➕ Add to Group** - Direct link to add the bot to a group
- **📖 Help** - Opens detailed help documentation

#### Second Row:
- **👨‍💻 Developer** - Link to contact the developer (@hasindu_2_0)
- **⭐ GitHub** - Link to the GitHub repository

## Interactive Features

### Help Button
When users click the "📖 Help" button:
- Displays detailed usage instructions
- Shows step-by-step guide
- Provides examples
- Includes a "🔙 Back" button to return to the main message

### Navigation
- Users can navigate between the welcome message and help documentation
- All interactions are smooth with inline keyboard updates

## Customization

### Change the Bot Image
Edit `handlers/start_command.py` line ~50:
```python
image_url = "YOUR_IMAGE_URL_HERE"
```

You can:
1. Upload an image to https://imgbb.com/ or https://postimg.cc/
2. Get the direct image URL
3. Replace the URL in the code

### Update Bot Username
Edit the "Add to Group" button URL in `handlers/start_command.py`:
```python
InlineKeyboardButton("➕ Add to Group", url="https://t.me/YOUR_BOT_USERNAME?startgroup=true")
```

### Update Developer Contact
Edit the developer link:
```python
InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/YOUR_USERNAME")
```

### Update GitHub Repository
Edit the GitHub link:
```python
InlineKeyboardButton("⭐ GitHub", url="https://github.com/YOUR_USERNAME/YOUR_REPO")
```

## Features

✅ **Personalized Greeting** - Uses the user's first name
✅ **Rich Formatting** - HTML formatting with bold, italic, and code blocks
✅ **Visual Appeal** - Includes an image for better presentation
✅ **Interactive Help** - Button-based navigation
✅ **Direct Actions** - Quick links to add bot to groups
✅ **Error Handling** - Fallback to text-only if image fails to load
✅ **Console Logging** - Tracks who uses the /start command

## Testing

1. Start a private chat with your bot on Telegram
2. Send `/start`
3. You should see:
   - The welcome image
   - Welcome message with bot info
   - Four inline buttons
4. Click "📖 Help" to see the help documentation
5. Click "🔙 Back" to return to the main message

## Console Output

When a user sends `/start`, you'll see in the console:
```
[START_COMMAND] User: John (@john123) | ID: 123456789
```

This helps you monitor bot usage and track new users.

## Notes

- The /start command works in **private chats only** (standard Telegram behavior)
- In groups, users should use the @admin command instead
- The image URL must be a direct link (ending in .png, .jpg, etc.)
- If the image fails to load, the bot will send the text message without the image
- All buttons are clickable and functional
- The help system uses callback queries for instant updates

## Troubleshooting

**Image doesn't show?**
- Verify the image URL is correct and publicly accessible
- Make sure it's a direct image link
- Try a different image hosting service

**Buttons don't work?**
- Check that callback handlers are registered in main.py
- Verify bot username in the "Add to Group" URL is correct

**Help button shows error?**
- Ensure all callback query handlers are properly registered
- Check console for error messages
