# event-helper

A Discord bot to track attendance in voice channels, providing real-time updates on current and upcoming attendees.


## 🛠️ Commands

- `/startwatching`: Begin monitoring a voice channel. The bot will provide updates on attendees.
- `/stopwatching`: Stop monitoring the voice channel. Updates on attendees will cease.


## 📦 Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/jenhere/event-helper.git
   cd event-helper
2. **Set up a virtual environment (optional but recommended)**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt


## ⚙️ Configuration
1. Create a Discord application and bot:
   - Navigate to the Discord Developer Portal.
   - Click on "New Application" and provide a name.
   - Under the "Bot" section, click "Add Bot" to create a bot user.
   - Copy the bot token; you'll need it for the next step.

2. Set up environment variables:
   Create a .env file in the root directory and add your bot token:
   ```env
   DISCORD_TOKEN=your_bot_token_here

3. Invite the bot to your server:
   - Go to the "OAuth2" section in your application settings.
   - Under "URL Generator", select the bot scope and the necessary permissions (e.g., Read Messages/View Channels, Send Messages, Connect, Speak).
   - Copy the generated URL and open it in your browser to invite the bot to your server.
  

## ▶️ Running the Bot
After completing the installation and configuration steps:
```bash
python main.py
