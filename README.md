# Telegram Bot & Group Chats messages through python

## Description
1. Building a simple Telegram Bot and then
2. Using a python script to send a predefined and preformatted message in all Telegram group chats that the bot is added. 

## Prerequisites
1. `python3` installed
2. `requests` module installed (`pip3 install requests`)
3. `dotenv` module with installed (`pip3 install python-dotenv`)

## Steps to setup & run

- `git clone` this repo


### Telegram Bot Settings
1. Download and install locally telegram app
2. Talk to Botfather & create your first bot (by following the steps described [here](https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot) (section "How to Create a New Bot for Telegram")
3. Copy the API Token of your bot
   Note : if you already have a bot, you can write `/mybots` to BotFather and it will return the name of your bot. Then you can click on button `API Token` and it will return the corresponding token.
4. Create a `.env` file in the root folder of this project/repository.
5. Paste your token in your `.env` file. The contents of your `.env` file should look like the following example :  
    ```
    API_KEY = "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"
    ```
6. Create at least one group chat in your telegram app and add your telegram bot. In this chat a message will be send from the bot through this python script (the script that will be executed in the "Run script" step).

### Update Group Message
1. You can edit the contents of the file `groupMessage.txt`(located in the `src` directory) and add the text of your choice.
2. You can format it as `Markdown` or `HTML` by using the tags mentioned [here](https://core.telegram.org/bots/api#markdownv2-style) and [here](https://core.telegram.org/bots/api#html-style) respectively.

### Run script
1. While in the root directory of this project, run command `python3 main.py` (from the terminal).

## Resources
- [Telegram Bot - how to get a group chat id?](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id)

## Short Walkthrough gif
![Recording](media/telegram-bot-python.gif "Short recording from the Telegram Bot + python script")
