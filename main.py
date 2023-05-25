from src.colors import *
from src.userConfirmation import *
from src.apiRequests import *

groupChats = getChatIds()

# Opens the groupMessage file which contains the text 
# we would like to send to the above retrieved group chats.
f = open("groupMessage.txt", "r")
groupMessage = f.read()

# Double check that the groupMessage.txt file contains the text
# you would like to convey to the above retrieved group chats.
print(yellow, "Group message that will be sent to the Group Chats", reset)
print(groupMessage)
question = "Is the group message correct ?"
reply = userConfirmation(question, default="no")
if reply == False:
  print(red, "Not Sending any Group Messages today! Nope! :( ", reset)
  sys.exit()

# print(yellow, "The group message will be sent to the following Group Chats", reset)
# for x in enumerate(groupChats):
#   print(groupChats)

question = "Are you sure you would like to send a group message to the above groups ?"
reply = userConfirmation(question, default="no")

if reply == True:
  sendGroupMessage(groupChats, groupMessage)
else:
  print(red, "Not Sending any Group Messages today! Nope! :( ", reset)
