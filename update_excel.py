import sys
import json
import os
from src.colors import *
from src.userConfirmation import *
from src.excelUpdater import *
from src.apiRequests import RESULTS_FILE

print(f"\n{DOUBLE_LINE}")
print(f"  {bold}{slate}Excel Tracker Update{reset}")
print(DOUBLE_LINE)

# Load last send results
if not os.path.exists(RESULTS_FILE):
  print(f"\n  {rose}No send results found. Run main.py first to send messages.{reset}\n")
  sys.exit()

with open(RESULTS_FILE, "r") as f:
  results = json.load(f)

# Show what was sent
sent = [k for k, v in results.items() if v]
failed = [k for k, v in results.items() if not v]

print(f"\n  {bold}{sand}Last send results ({len(results)} group{'s' if len(results) != 1 else ''}):{reset}")
for chat_id, success in results.items():
  status = f"{sage}Yes{reset}" if success else f"{rose}No{reset}"
  print(f"  {stone}  {chat_id}: {status}{reset}")

print(f"\n  {sage}{len(sent)} sent{reset}, {rose}{len(failed)} failed{reset}")

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
