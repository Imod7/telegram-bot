import os
import requests
from src.colors import *
from dotenv import load_dotenv, find_dotenv

# Your API_KEY should be saved in the same directory in a file called .env
# which contains one line of text with the following format
# API_KEY = "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"
load_dotenv(find_dotenv())
API_KEY = os.environ.get("API_KEY")

# Function that sends the groupMessage through our bot to all the telegram group chats.
def sendGroupMessage(groupChats, groupMessage):
  sendMsgUrl = "https://api.telegram.org/bot" + API_KEY + "/sendMessage"
  print("Sending to Group Chats :") 
  for key, value in groupChats.items():
    print(green, "✅", value)
    send_text = 'https://api.telegram.org/bot' + API_KEY + '/sendMessage?chat_id=' + str(key) + '&parse_mode=HTML&text=' + groupMessage
    response = requests.get(send_text)
