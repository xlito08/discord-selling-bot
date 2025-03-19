# Discord Bot for Vouches, Embeds & Role Management

## 📌 Description
This Discord bot provides various functionalities for managing vouches, creating embed messages, and handling role assignments. It is built with **Python** using the `discord.py` library and features **slash commands**, JSON-based data storage, and role-based access control.

## ✨ Features
- ✅ **Vouch System** – Users can submit and restore vouches with star ratings and proof images.
- 📦 **Product Embeds** – Predefined embeds for digital services like Spotify, Netflix, and YouTube Premium.
- 🎭 **Role Management** – Assign customer roles with a simple command.
- 🎨 **Custom Embed Creator** – Generate personalized embeds with titles, descriptions, images, and colors.
- 🧹 **Message Cleanup** – Bulk delete messages for easy moderation.

## 🚀 Installation Guide

### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/xlito08/discord-selling-bot.git
cd discord-selling-bot
```

### 2️⃣ **Install Dependencies**
Ensure you have Python installed (recommended version **3.8 or higher**). Then install the required packages:
```sh
pip install -r requirements.txt
```

### 3️⃣ **Create & Configure `config.json`**
In the root directory, create a file named **`config.json`** and fill it with your bot credentials and settings:
```json
{
  "bot_token": "YOUR_DISCORD_BOT_TOKEN",
  "required_role_id": 123456789012345678,
  "restore_allowed_users": [123456789012345678],
  "allowed_channel_id": 123456789012345678,
  "embed_required_role_id": 123456789012345678,
  "customer_role_id": 123456789012345678,
  "create_embed_allowed_users": ["123456789012345678"]
}
```
Replace the placeholders with the actual **Discord Bot Token** and Role/Channel/User IDs.

### 4️⃣ **Run the Bot**
Simply execute the provided **`start.bat`** file:
```sh
start.bat
```
Or manually run:
```sh
python bot.py
```

## 🤖 How to Create a Discord Bot
1. **Go to the [Discord Developer Portal](https://discord.com/developers/applications)**.
2. Click **New Application**, give it a name, and create it.
3. Navigate to **Bot** (left menu) → Click **Add Bot**.
4. Copy the **Token** and paste it into your `config.json` file.
5. Under **OAuth2 → URL Generator**, select `bot` and `applications.commands` scopes.
6. Assign the necessary **permissions** and generate the bot invite link.
7. Invite the bot to your server and run it.

## 🛠️ Implementation Details
- **Language:** Python
- **Library:** `discord.py`
- **Data Storage:** JSON files (`vouches.json`, `product-embeds.json`, `config.json`)
- **Security:** Role-based access control for restricted commands
- **Error Handling:** Checks for permissions, missing configurations, and invalid user actions

## 📜 Commands List
| Command | Description |
|---------|-------------|
| `/vouch` | Submit a vouch with rating and proof |
| `/vouch-restore` | Restore all stored vouches |
| `/embed` | Create a predefined product embed |
| `/give-customer` | Assign the customer role to a user |
| `/create-embed` | Generate a custom embed |
| `/clear` | Delete a specified number of messages |

## 📞 Support & Contributions
Feel free to open an **issue** or create a **pull request** if you find a bug or want to contribute!

🔗 **GitHub Repository:** [https://github.com/xlito08/discord-selling-bot]

© 2025 LTXX — All Rights Reserved.
