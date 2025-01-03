
## Telegram Scraper Bot

I needed a tool to help me track down a pair of shoes i've been wanting for a while. I decided to build a Telegram bot that would scrape the website for me and notify me when the shoes are in stock. This bot is designed to monitor specific sizes and notify the user about their stock status periodically.

---

### Features
- Scrapes product sizes and availability from a given website.
- Sends Telegram messages with stock details, including product links for in-stock items.
- Scheduled to run 6 times a day at 4-hour intervals.

---

### Requirements
- Python 3.7 or higher
- Telegram bot API token and chat ID

---

### Setup Instructions

#### 1. Clone the Repository
```bash
git clone https://github.com/IlanBrof/CloudTiltStock_bot.git
cd CloudTiltStock_bot
```

#### 2. Create a Virtual Environment
```bash
python -m venv venv
```

Activate the environment:
- **Windows**: `venv\Scripts\activate`
- **Linux/Mac**: `source venv/bin/activate`

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables
Create a `.env` file in the project root with the following content:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

Replace `your_telegram_bot_token` and `your_chat_id` with your actual Telegram bot token and chat ID.

#### 5. Run the Bot
Start the bot by running:
```bash
python cloudTilt_bot.py
```

The bot will run in the background, scraping the website and sending notifications to your Telegram chat.

---

### Project Structure
```
telegram-scraper-bot/
│
├── .env                # Environment variables (not included in the repo)
├── .gitignore          # Files to ignore in version control
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies
├── main.py             # Main bot script
├── constants.py        # Constants such as URLs
└── venv/               # Virtual environment (not included in the repo)
```

---

### Scheduling
The bot is scheduled to scrape the website at the following times daily:
- `00:00`
- `04:00`
- `08:00`
- `12:00`
- `16:00`
- `20:00`

---

### Example Telegram Message
```
Shoe Color: Black Ivory
  Size 42.5: In Stock (https://ingsport.co.il/products/cloudtilt-black-ivory)
  Size 43: Sold Out

Shoe Color: Eclipse Black
  Size 42.5: Sold Out
  Size 43: In Stock (https://ingsport.co.il/products/cloudtilt-eclipse-black)
```

---

### Notes
- Ensure the `.env` file is excluded from version control to keep sensitive information secure.
- For any issues or contributions, feel free to submit a pull request or open an issue.
