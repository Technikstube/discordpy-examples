# Modmail Bot Example

A simple Modmail bot example for Discord that allows users to contact server moderators via direct messages. The bot creates a private ticket channel for each conversation, allowing staff to respond directly.

**Features**
Modmail Ticketing: Users can send direct messages to the bot, which creates a private ticket channel on the server.
Auto Channel Creation: Automatically creates a "Modmail Tickets" category and a channel for each user.
Message Forwarding: User messages are forwarded to the ticket channel, and staff replies are sent back to the user.
Ticket Closure: Staff can close tickets with the -close command, which also sends the user a transcript of the conversation.

**Installation**
1. Install Python: Ensure Python 3.7+ is installed.
2. Install Dependencies: Run pip install discord.
3. Set Up Bot: Create a bot on the Discord Developer Portal, and add the bot token to your script.
4. Run the Bot: Start the bot using your script.

**Usage**
Add the bot to your Discord server.
Ensure the bot has permissions to read/send messages, manage channels, and send files.
Users can DM the bot to create a ticket. Staff can reply in the created channel and close it with -close.

