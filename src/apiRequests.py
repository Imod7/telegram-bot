import os
import requests
from src.colors import *
from dotenv import load_dotenv, find_dotenv

# Your API_KEY should be saved in the same directory in a file called .env
# which contains one line of text with the following format
# API_KEY = "980776865:hgjafhuergaenbvunxzvjawh"
load_dotenv(find_dotenv())
API_KEY = os.environ.get("API_KEY")

# Function that retrieves the chat_ids of all the group chats
# in which the bot is included
def getChatIds():
  getUpdatesUrl = "https://api.telegram.org/bot" + API_KEY + "/getUpdates"
  response = requests.get(getUpdatesUrl)
  jsonResponse = response.json()
  groupChats = {}
  for x in jsonResponse['result']:
    if (x['message']['chat']['type'] == 'group'):
      groupChats[x['message']['chat']['id']] = x['message']['chat']['title']
  return groupChats

# Function that sends the groupMessage through our bot to all the telegram group chats.
def sendGroupMessage(groupChats, groupMessage):
  sendMsgUrl = "https://api.telegram.org/bot" + API_KEY + "/sendMessage"
  for key in groupChats:
    print(green, "Sending to Group Chat : ", groupChats[key], reset)
    parameters = {
      "chat_id" : key,
      "text" : groupMessage,
      "parse_mode" : "html"
    }
    response = requests.get(sendMsgUrl, data = parameters)