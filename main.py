from src.colors import *
from src.userConfirmation import *
from src.apiRequests import *

print(f"\n{DOUBLE_LINE}")
print(f"  {bold}{slate}Telegram Group Message Sender{reset}")
print(DOUBLE_LINE)

# Read the message file
f = open("files/groupMessage.txt", "r")
groupMessage = f.read()

# Show the message that will be sent
print(f"\n  {bold}{sand}Message Preview:{reset}")
print(LINE)
for line in groupMessage.splitlines():
  print(f"  {stone}|{reset} {line}")
print(LINE)

# Confirm the message content
question = "Is this message correct?"
reply = userConfirmation(question, default="no")
if reply == False:
  print(f"\n  {rose}Cancelled. No messages were sent.{reset}\n")
  sys.exit()

print(f"\n  {sage}Message confirmed.{reset}")

# Retrieving the group chats from the groups.txt file.
groupChats = {}
with open('files/groups.txt') as f:
  lines = f.readlines()
  for line in lines:
    currentline = line.split(",")
    groupChats[currentline[0]] = currentline[1]

if len(groupChats) == 0:
  print(f"\n  {rose}No groups found in groups.txt. Nothing to send.{reset}\n")
  sys.exit()

# Show the target groups
print(f"\n  {bold}{sand}Recipients ({len(groupChats)} group{'s' if len(groupChats) != 1 else ''}):{reset}")
for i, (key, value) in enumerate(groupChats.items(), 1):
  print(f"  {teal}  {i}. {value.strip()}{reset}")

# Confirm sending
question = "Send the message to these groups?"
reply = userConfirmation(question, default="no")

# Based on the previous answers the message will be sent or not.
if reply == True:
  sendGroupMessage(groupChats, groupMessage)
else:
  print(f"\n  {rose}Cancelled. No messages were sent.{reset}\n")
