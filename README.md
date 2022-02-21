# Telegram Bot & Group Chats messages through python

## Description
1. Building a simple Telegram Bot and then
2. Using a python script to send a predefined and preformatted message in all Telegram group chats that the bot is added. 

## Prerequisites
1. `python3` installed
2. `requests` module installed
3. `dotenv` module with installed (`pip3 install python-dotenv`)

## Telegram Bot Settings
1. Download and install locally telegram app
2. Talk to Botfather & create your first bot (by following the steps described [here](https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot) (section "How to Create a New Bot for Telegram")
3. Save your bots API key in a `.env` file that you add in the root directory.
4. Your `.env` file chould contain one line of text with the following format `API_KEY = "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`

## Update Group Message
1. You can edit the contents of the file `groupMessage.txt`(located in the `src` directory) and add the text of your choice.
2. You can format it as `Markdown` or `HTML` by using the tags mentioned [here](https://core.telegram.org/bots/api#markdownv2-style) and [here](https://core.telegram.org/bots/api#html-style) respectively.

## Run script
1. `git clone` this repo
2. Run command `python3 main.py` on terminal

### Short Walkthrough gif
![Recording](media/telegram-bot-python.gif "Short recording from the Telegram Bot + python script")