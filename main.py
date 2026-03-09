import os
from src.colors import *
from src.userConfirmation import *
from src.apiRequests import *
from src.excelUpdater import EXCEL_PATH

print(f"\n{DOUBLE_LINE}")
print(f"  {bold}{slate}Telegram Group Message Sender{reset}")
print(DOUBLE_LINE)

# Check if the Excel tracking file exists
update_excel = False
if os.path.exists(EXCEL_PATH):
  print(f"\n  {sage}Excel file found:{reset} {stone}{EXCEL_PATH}{reset}")
  question = "Update the Excel tracker after sending?"
  update_excel = userConfirmation(question, default="no")
else:
  print(f"\n  {sand}No Excel file found at {EXCEL_PATH}")
  print(f"  {stone}Skipping Excel tracking.{reset}")

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
if reply != True:
  print(f"\n  {rose}Cancelled. No messages were sent.{reset}\n")
  sys.exit()

results = sendGroupMessage(groupChats, groupMessage)

# Update Excel if the user opted in at the start
if not update_excel:
  print(f"\n  {stone}Done. Excel update was skipped.{reset}\n")
  sys.exit()

from src.excelUpdater import getAvailableColumns, updateExcel

# Show available columns and ask which one to update
columns = getAvailableColumns()
print(f"\n  {bold}{sand}Available columns:{reset}")
for letter, header in columns:
  print(f"  {teal}  {letter}: {header}{reset}")

print(f"\n  {bold}Enter the column letter to update (e.g. AI):{reset} ", end="")
col = input().strip().upper()

# Validate the column letter
valid_letters = [letter for letter, _ in columns]
if col not in valid_letters:
  print(f"\n  {rose}Invalid column '{col}'. Excel not updated.{reset}\n")
  sys.exit()

# Show which column was selected
header = next(h for l, h in columns if l == col)
print(f"  {stone}Selected: {col} ({header}){reset}")

question = f"Write results to column {col}?"
reply = userConfirmation(question, default="no")

if reply == True:
  updated = updateExcel(results, col)
  print(f"\n  {sage}{bold}Excel updated — {updated} row(s) written in column {col}.{reset}\n")
else:
  print(f"\n  {stone}Excel not updated.{reset}\n")
