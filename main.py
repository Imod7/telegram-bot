from src.colors import *
from src.userConfirmation import *
from src.apiRequests import *

f = open("files/groupMessage.txt", "r")
groupMessage = f.read()

# Question to confirm that the groupMessage.txt file contains the message
# we would like to send to the group chats.
print(yellow, "Group message that will be sent to the Group Chats", reset)
print(groupMessage)
question = "Is the group message correct ?"
reply = userConfirmation(question, default="no")
if reply == False:
  print(red, "Not Sending any Group Messages today! Nope! :( ", reset)
  sys.exit()

# Retrieving the group chats from the groups.txt file.
groupChats = {}
print(yellow, "The group message will be sent to the following Group Chats", reset)
with open('files/groups.txt') as f:
  lines = f.readlines()
  for line in lines:
    currentline = line.split(",")
    groupChats[currentline[0]] = currentline[1]

for key, value in groupChats.items():
  print(value)

# Question to confirm that the message will be sent to the correct group chats.
question = "Are you sure you would like to send a group message to the above groups ?"
reply = userConfirmation(question, default="no")

# Based on the previous answers the message will be sent or not.
if reply == True:
  sendGroupMessage(groupChats, groupMessage)
else:
  print(red, "Not Sending any Group Messages today! Nope! :( ", reset)
