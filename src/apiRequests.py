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
  total = len(groupChats)
  success = 0
  failed = 0

  print(f"\n{LINE}")
  print(f"  {bold}{slate}Sending messages...{reset}")
  print(LINE)

  for i, (key, value) in enumerate(groupChats.items(), 1):
    payload = {
      "chat_id": str(key),
      "parse_mode": "HTML",
      "text": groupMessage,
    }
    response = requests.post(sendMsgUrl, json=payload)
    if response.ok:
      print(f"  {sage}  [{i}/{total}] Sent to {value.strip()}{reset}")
      success += 1
    else:
      error = response.json().get("description", response.text)
      print(f"  {rose}  [{i}/{total}] Failed: {value.strip()} - {error}{reset}")
      failed += 1

  # Summary
  print(f"\n{DOUBLE_LINE}")
  if failed == 0:
    print(f"  {sage}{bold}All {success} message(s) sent successfully!{reset}")
  elif success == 0:
    print(f"  {rose}{bold}All {failed} message(s) failed to send.{reset}")
  else:
    print(f"  {sand}{bold}Results: {sage}{success} sent{reset}{bold}, {rose}{failed} failed{reset}")
  print(DOUBLE_LINE)
