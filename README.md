# Algo-Trading System with ML & Automation

## Overview

This is a Python-based mini algo-trading prototype that:
- Fetches daily stock data of NIFTY 50 stocks via Yahoo Finance API.
- Implements a trading strategy combining RSI and Moving Average crossover.
- Trains a Logistic Regression ML model to predict next-day price movement.
- Logs trade signals and analytics to Google Sheets.
- Sends real-time buy/sell alerts via Telegram bot.
- Modular, automated, and designed for easy scheduling and extension.

---

## Setup Instructions

1. **Clone the repository or extract the ZIP** to your local machine.

2. **Install Python 3.7 or higher** if not installed.

3. **Install required Python packages**:


4. **Google Sheets API setup**:

- Create a Google Cloud project.
- Enable Google Sheets API.
- Create a service account and download the JSON credentials file named `creds.json`.
- Share your Google Sheet with the service account email (edit permissions).

5. **Telegram Bot setup**:

- Create a Telegram bot via [@BotFather](https://t.me/BotFather).
- Save the provided Bot Token.
- Start a chat with your bot.
- Get your Telegram chat ID by visiting:  
  `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
- Find `"chat": {"id": ...}` in the response; this is your chat ID.
## Strategy Description

The implemented strategy generates buy signals under these conditions:

- **RSI Indicator**: RSI value is less than 30 (oversold condition).
- **Moving Average Crossover**: 20-day moving average crosses above 50-day moving average on that day.

Signals are backtested on 6 months of historical daily stock data for selected NIFTY 50 stocks (`RELIANCE.NS`, `HDFCBANK.NS`, `INFY.NS`).

The ML model uses Logistic Regression with features:

- RSI
- MACD and MACD signal
- Volume

to predict whether the next day’s closing price will rise.

---

## How to Run the Code

1. Open `main.py`.

2. Replace the placeholder values:

3. Run the script:


4. Monitor:

- Console output for buy signals and ML accuracy.
- Google Sheets tabs for logged signals and analytics.
- Telegram for real-time buy signal and model accuracy alerts.

---

## API Key Configuration Steps

### Google Sheets Credentials

- Save your Google service account credentials JSON file as `creds.json` in the project root.
- Make sure your Google Sheet is shared with the service account’s client email address.
- The sheets logger module reads this file to authenticate and write data.

### Telegram Bot Credentials

- Obtain your Telegram Bot Token from BotFather.
- Start a conversation with your bot in the Telegram app by sending `/start`.
- Use the Telegram Bot API’s `getUpdates` endpoint to find your numeric chat ID.
- Set the token and chat ID in `main.py`.

---

## Additional Notes

- The system batches Telegram messages with controlled delays to avoid API limits.
- Multi-index columns from Yahoo Finance are flattened for compatibility.
- You can extend features, add P&L calculations, and tune the ML model for improved performance.
- Schedule `main.py` via a cron job or Windows Task Scheduler for automation.


