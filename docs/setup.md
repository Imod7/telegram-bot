# Setup & Bot Configuration

One-time setup. After this, day-to-day use is just the [Quick Start](../README.md#quick-start--sending-a-message-do-this-every-time).

## Prerequisites

- **Python 3** — Install via [python.org](https://www.python.org/) or Homebrew (`brew install python3`)
- **pip3** — Typically bundled with Python 3; otherwise `brew install pip3`
- **virtualenv** — `pip3 install virtualenv`

## Install

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd telegram-bot
   ```
2. Create and activate a virtual environment:
   ```bash
   virtualenv env-telegram-bot
   source env-telegram-bot/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

## Telegram Bot Configuration

1. Download and install the [Telegram Desktop App](https://desktop.telegram.org/).
2. Create a new bot by messaging [BotFather](https://t.me/botfather).
   - Guide: [How to Create and Connect a Telegram Chatbot](https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot).
3. Obtain the API token.
   - For an existing bot, send `/mybots` to BotFather, select the bot, and click **API Token**.
4. Create a `.env` file in the project root:
   ```bash
   touch .env
   ```
5. Add your token in this format:
   ```
   API_KEY = "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"
   ```
6. Create at least one Telegram group chat and add your bot as a member. That group will receive the message when the script runs.

Next: add your recipient groups — see [Recipient Groups](./recipients.md).
