import os
from src.colors import *
from src.userConfirmation import *
from src.apiRequests import *
from src.excelUpdater import promptExcelPath

print(f"\n{DOUBLE_LINE}")
print(f"  {bold}{slate}Telegram Group Message Sender{reset}")
print(DOUBLE_LINE)

# Ask whether to update an Excel tracker, and if so which file
excel_path = None
question = "Update an Excel tracker after sending?"
update_excel = userConfirmation(question, default="no")
if update_excel:
  excel_path = promptExcelPath()
  if os.path.exists(excel_path):
    print(f"  {sage}Excel file found:{reset} {stone}{excel_path}{reset}")
  else:
    print(f"\n  {sand}No Excel file found at {excel_path}")
    print(f"  {stone}Skipping Excel tracking.{reset}")
    update_excel = False

# Read the Telegram message (generated from files/message.md by format_message.py)
TELEGRAM_MESSAGE_FILE = "files/out/telegram.html"
if not os.path.exists(TELEGRAM_MESSAGE_FILE):
  print(f"\n  {rose}No Telegram message found at {TELEGRAM_MESSAGE_FILE}.{reset}")
  print(f"  {stone}Write your message in files/message.md, then run: python3 format_message.py{reset}\n")
  sys.exit()
with open(TELEGRAM_MESSAGE_FILE, "r") as f:
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

# Resume support: if a previous run left a results file, offer to skip the
# groups already sent successfully and send only the remaining ones
# (previously failed + never attempted). Groups whose delivery was UNCERTAIN
# (timed out mid-send) are held back from auto-resend and flagged, since
# re-sending them could duplicate a message that already arrived.
import datetime
prior_results = loadPriorResults()
prior_ambiguous = loadAmbiguous()
already_sent = {k for k, ok in prior_results.items() if ok}
ambiguous_ids = {k for k in prior_ambiguous if k in groupChats}
sendChats = {k: v for k, v in groupChats.items()
             if k not in already_sent and k not in ambiguous_ids}
seed = None
seed_ambiguous = None

if (already_sent or ambiguous_ids) and len(sendChats) < len(groupChats):
  mtime = datetime.datetime.fromtimestamp(os.path.getmtime(RESULTS_FILE))
  print(f"\n  {bold}{sand}Previous send found{reset} {stone}(last updated {mtime:%Y-%m-%d %H:%M}){reset}")
  print(f"  {sage}  {len(already_sent)} group(s) already sent successfully{reset}")
  print(f"  {teal}  {len(sendChats)} group(s) remaining (not-yet-sent + previously failed){reset}")
  if ambiguous_ids:
    print(f"  {sand}  {len(ambiguous_ids)} group(s) with UNCERTAIN delivery (timed out — verify manually):{reset}")
    for k in ambiguous_ids:
      print(f"  {sand}    • {groupChats[k].strip()}{reset}")

  resume = userConfirmation(
    f"Resume — skip the {len(already_sent)} already sent and send only the {len(sendChats)} remaining?",
    default="no",
  )
  if resume:
    seed = prior_results
    seed_ambiguous = prior_ambiguous
    # The uncertain ones are held back by default. Offer to re-send anyway.
    if ambiguous_ids and userConfirmation(
        f"Also re-send to the {len(ambiguous_ids)} UNCERTAIN group(s)? (may duplicate)",
        default="no"):
      for k in ambiguous_ids:
        sendChats[k] = groupChats[k]
  elif userConfirmation("Start fresh instead — send to ALL groups (resets the record)?", default="no"):
    sendChats = groupChats
    seed = None
    seed_ambiguous = None
  else:
    print(f"\n  {rose}Cancelled. No messages were sent.{reset}\n")
    sys.exit()

if len(sendChats) == 0:
  print(f"\n  {sage}Nothing to send — all groups already sent (or held for manual check).{reset}\n")
  sys.exit()

# Show the target groups
print(f"\n  {bold}{sand}Recipients ({len(sendChats)} group{'s' if len(sendChats) != 1 else ''}):{reset}")
for i, (key, value) in enumerate(sendChats.items(), 1):
  print(f"  {teal}  {i}. {value.strip()}{reset}")

# Confirm sending
question = "Send the message to these groups?"
reply = userConfirmation(question, default="no")

# Based on the previous answers the message will be sent or not.
if reply != True:
  print(f"\n  {rose}Cancelled. No messages were sent.{reset}\n")
  sys.exit()

results = sendGroupMessage(sendChats, groupMessage, prior_results=seed, prior_ambiguous=seed_ambiguous)

# Update Excel if the user opted in at the start
if not update_excel:
  print(f"\n  {stone}Done. Excel update was skipped.{reset}\n")
  sys.exit()

from src.excelUpdater import getAvailableColumns, updateExcel, columnHasData

# Show available columns and ask which one to update
columns = getAvailableColumns(excel_path)
if len(columns) == 0:
  print(f"\n  {rose}No columns found in the sheet. Excel not updated.{reset}\n")
  sys.exit()

print(f"\n  {bold}{sand}Available columns:{reset}")
for letter, header in columns:
  print(f"  {teal}  {letter}: {header}{reset}")

# Default to the last column in the sheet (usually the newest tracking column)
default_col, default_header = columns[-1]
print(f"\n  {bold}Column to update{reset} {stone}[{default_col}: {default_header}]{reset}")
print(f"  {stone}Press Enter to keep the last column, or type a different letter:{reset} ", end="")
col = input().strip().upper()
if not col:
  col = default_col

# Validate the column letter
valid_letters = [letter for letter, _ in columns]
if col not in valid_letters:
  print(f"\n  {rose}Invalid column '{col}'. Excel not updated.{reset}\n")
  sys.exit()

# Show which column was selected
header = next(h for l, h in columns if l == col)
print(f"  {stone}Selected: {col} ({header}){reset}")

# Warn before overwriting a column that already has data
if columnHasData(excel_path, col):
  print(f"\n  {sand}Warning: column {col} ({header}) already has data and will be overwritten.{reset}")
  if userConfirmation(f"Overwrite existing values in column {col}?", default="no") != True:
    print(f"\n  {stone}Excel not updated.{reset}\n")
    sys.exit()

question = f"Write results to column {col}?"
reply = userConfirmation(question, default="no")

if reply == True:
  updated = updateExcel(results, col, excel_path)
  print(f"\n  {sage}{bold}Excel updated — {updated} row(s) written in column {col}.{reset}\n")
else:
  print(f"\n  {stone}Excel not updated.{reset}\n")
