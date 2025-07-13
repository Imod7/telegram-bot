# Telegram Bot & Group Chats messages through python

## Description
This project guides you through on how to :
1. Build a simple Telegram Bot and then
1. Use a python script to send a predefined and preformatted message in all Telegram group chats that the bot is added.

## Prerequisites
1. Install `python3` (if you already have `brew` you can use `brew install python3` to install it)
1. Install `pip3` (if you already have `brew` you can use `brew install pip3` to install it)
1. Install `virtualenv` with `pip3 install virtualenv`

## Steps to setup & run
- `git clone` this repo
- `cd telegram-bot`
- create a new virtual environment with a name of your choice (e.g. `env-telegram-bot`) by typing the following command :
    ```
    virtualenv env-telegram-bot
    ```
- activate the virtual environment you just created with the command :
    ```
    source env-telegram-bot/bin/activate
    ```
- use command `pip3 install -r requirements.txt` to install all required packages.

### Telegram Bot Setup
1. Download and install locally the [Telegram Desktop App](https://desktop.telegram.org/)
1. Talk to Botfather & create your first bot
    - Note: You can follow the steps described in the guide [How to Create and Connect a Telegram Chatbot](https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot).
1. Copy the API Token of your bot
   - Note : if you already have a bot, you can write `/mybots` to BotFather and it will return the name of your bot. Then you can click on button `API Token` and it will return the corresponding token.
1. Create an `.env` file in the root folder of this project/repository (folder `telegram-bot`). You can do that with command the `touch .env` command.
1. Open your `.env` file and your token of your bot. The contents of your `.env` file should look like the following example :
    ```
    API_KEY = "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"
    ```
1. Create at least one group chat in your telegram app and add your telegram bot. In this chat a message will be send from the bot through this python script (the script that will be executed in the "Run script" step).

### Update Group Message file
1. You can edit the contents of the file `groupMessage.txt`(located in the `files` directory) and add the text of your choice.
1. You can format it as `Markdown` or `HTML` by using the tags mentioned [here](https://core.telegram.org/bots/api#markdownv2-style) and [here](https://core.telegram.org/bots/api#html-style) respectively.

### Add the Group Chats file
1. You can add the group chats that you want to send the message to in the file `groups.txt`(located in the `files` directory).
1. The format should be `-TelegramChatID, TelegramChatName`, e.g. `-123456789, MyGroupChatName`.
1. If you have multiple group chats you would like to send the message to, you can add them in new lines.


### Add the Chatbot to a new Group Chat
If the chatbot needs to be added to a new group chat (that is not included in the `groups.txt` file), you can do the following:
1. You can add the bot to the group as you would add any member to the telegram group chat.
1. Then you need to retrieve the corresponding group chat id.
1. You do this by following this guide [Telegram Bot - how to get a group chat id?](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id)

    ```
    https://api.telegram.org/bot<YourBOTToken>/getUpdates
    ```

CAUTION
- Sometimes when you add the chatbot into a new group chat and I go the `getUpdates` endpoint does not work and is showing a blank page so no group chat ids. 
- In this case you can use a hacky way to retrieve it.
- Just go into one of the test groups where the chatbot is already added, remove the chatbot and add it again. 
- Then the endpoint for some reason gets updated and you can see the full list of group chat ids where it is included.
- If you search the page based on the name of the new group chat, you can find the corresponding entry and copy the chat id.
- Then you can also add this chat id in the `groups.txt` file to have it ready for future use.

### Recommended Last Checks
1. Always send the msg to a test group (e.g. the Integration Testing Playground group) first to check that the message is sent correctly. Then you can send to the designated groups all at once.
1. If you notice that the message is sent for example half or not at all, this might be related to the formatting so check the file `groupMessage.txt`` and look for special characters (like &) that might interfere with the HTML formatting (which is currently set in the script). Replace the problematic character with the corresponding character in HTML specification.


### Run script
1. While in the root directory of this project, run command `python3 main.py` (from the terminal).
1. Check in the corresponding Telegram chats if the message was posted successfully and with the expected formatting.
1. When you are finished with the script, you can deactivate the virtual environment with the command :
    ```
    deactivate
    ```

## Maintenance
Ensure all dependencies are up to date. To check for new updates, run:
```
pip list --outdated
```

For each outdated package, run the command:
```
pip install --upgrade <package_name>
```

After updating all packages, save the current versions in the `requirements.txt` file by running:
```
pip freeze > requirements.txt
```

## Troubleshooting
- If you get a `ModuleNotFoundError: No module named 'requests'` error when running `python3 main.py`, it indicates that the virtual environment is not activated. To resolve this, activate the virtual environment with `source env-telegram-bot/bin/activate`.
- If the message is not sent to one of the Telegram groups included in the list, use `https://api.telegram.org/bot<YourBOTToken>/getUpdates` in your browser to verify the group/chat ID. If the chat ID is incorrect, update it with the correct one.
- When sending messages through Telegram, you need to replace special characters like `#` (with `%23`) in the `groupMessage.txt` otherwise the message will be sent half. Also, `&` might need to be replaced.

## Short Walkthrough gif
![Recording](media/telegram-bot-python.gif "Short recording from the Telegram Bot + python script")
