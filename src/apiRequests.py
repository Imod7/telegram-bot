import os
import json
import requests
from requests.exceptions import RequestException, ReadTimeout
from src.colors import *
from dotenv import load_dotenv, find_dotenv

RESULTS_FILE = "files/last_send_results.json"
AMBIGUOUS_FILE = "files/last_send_ambiguous.json"

# Network settings so a dropped/hung connection can never block the run forever.
TIMEOUT = (10, 30)   # (connect, read) seconds
MAX_ATTEMPTS = 3     # connect-phase retries, before giving up on a group

# Your API_KEY should be saved in the same directory in a file called .env
# which contains one line of text with the following format
# API_KEY = "110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"
load_dotenv(find_dotenv())
API_KEY = os.environ.get("API_KEY")


# Load the results of a previous run (chat_id -> True/False), or {} if none.
# Used to resume an interrupted send without re-sending to groups already done.
def loadPriorResults():
  return _loadJsonDict(RESULTS_FILE)


# Load the groups whose delivery was UNCERTAIN in a previous run
# (chat_id -> group name). These timed out after the request was sent, so the
# message may or may not have arrived and should be checked manually.
def loadAmbiguous():
  return _loadJsonDict(AMBIGUOUS_FILE)


def _loadJsonDict(path):
  if not os.path.exists(path):
    return {}
  try:
    with open(path) as f:
      data = json.load(f)
    return data if isinstance(data, dict) else {}
  except (json.JSONDecodeError, OSError):
    return {}


# POST with a timeout. Returns (response, error).
#
# A ReadTimeout means the request was sent but no response came back — the
# message MAY already have been delivered, so we do NOT retry (retrying could
# duplicate it) and let the caller flag it as uncertain. Any other error
# (e.g. connect failure) means the request never reached Telegram, so it is
# safe to retry a few times before giving up.
def _postWithRetry(url, payload):
  last_err = None
  for attempt in range(1, MAX_ATTEMPTS + 1):
    try:
      return requests.post(url, json=payload, timeout=TIMEOUT), None
    except ReadTimeout as e:
      return None, e  # ambiguous — do not retry
    except RequestException as e:
      last_err = e    # connect/other — safe to retry
  return None, last_err


# Function that sends the groupMessage through our bot to all the telegram group chats.
# Returns a dict of {chat_id: True/False} for each group.
# `prior_results` seeds the saved record so a resumed run keeps the groups that
# were already sent in a previous run (they are not re-sent here — the caller
# passes only the groups still pending).
# `prior_ambiguous` seeds the uncertain-delivery record (chat_id -> name); a
# clean send/fail this run clears a group from it, a timeout adds it.
def sendGroupMessage(groupChats, groupMessage, prior_results=None, prior_ambiguous=None):
  sendMsgUrl = "https://api.telegram.org/bot" + API_KEY + "/sendMessage"
  total = len(groupChats)
  success = 0
  failed = 0
  uncertain = 0
  # Start from the prior records so both files stay complete across resumes.
  results = dict(prior_results) if prior_results else {}
  ambiguous = dict(prior_ambiguous) if prior_ambiguous else {}

  def persist():
    with open(RESULTS_FILE, "w") as rf:
      json.dump(results, rf, indent=2)
    with open(AMBIGUOUS_FILE, "w") as af:
      json.dump(ambiguous, af, indent=2)

  print(f"\n{LINE}")
  print(f"  {bold}{slate}Sending messages...{reset}")
  print(LINE)

  try:
    for i, (key, value) in enumerate(groupChats.items(), 1):
      name = value.strip()
      payload = {
        "chat_id": str(key),
        "parse_mode": "HTML",
        "text": groupMessage,
      }
      response, err = _postWithRetry(sendMsgUrl, payload)
      if isinstance(err, ReadTimeout):
        # Request was sent but no response — delivery is UNCERTAIN. Do not
        # count as sent; flag for manual verification.
        print(f"  {sand}  [{i}/{total}] TIMEOUT — delivery UNCERTAIN, check manually: {name}{reset}")
        uncertain += 1
        results[key] = False
        ambiguous[key] = name
      elif err is not None:
        print(f"  {rose}  [{i}/{total}] Failed (not delivered): {name} - network error: {err}{reset}")
        failed += 1
        results[key] = False
        ambiguous.pop(key, None)
      elif response.ok:
        print(f"  {sage}  [{i}/{total}] Sent to {name}{reset}")
        success += 1
        results[key] = True
        ambiguous.pop(key, None)
      else:
        error = response.json().get("description", response.text)
        print(f"  {rose}  [{i}/{total}] Failed: {name} - {error}{reset}")
        failed += 1
        results[key] = False
        ambiguous.pop(key, None)
      # Persist after every send so an interrupt (Ctrl+C) never loses progress
      persist()
  except KeyboardInterrupt:
    print(f"\n  {sand}Interrupted. {success + failed + uncertain}/{total} attempted this run; "
          f"progress saved. Re-run to resume the remaining groups.{reset}")
    _reportAmbiguous(ambiguous)
    return results

  # Summary
  print(f"\n{DOUBLE_LINE}")
  if failed == 0 and uncertain == 0:
    print(f"  {sage}{bold}All {success} message(s) sent successfully!{reset}")
  elif success == 0 and uncertain == 0:
    print(f"  {rose}{bold}All {failed} message(s) failed to send.{reset}")
  else:
    parts = [f"{sage}{success} sent{reset}{bold}"]
    if failed:
      parts.append(f"{rose}{failed} failed{reset}{bold}")
    if uncertain:
      parts.append(f"{sand}{uncertain} uncertain{reset}{bold}")
    print(f"  {bold}Results: " + ", ".join(parts) + f"{reset}")
  print(DOUBLE_LINE)

  print(f"  {stone}Results saved to {RESULTS_FILE}{reset}")
  _reportAmbiguous(ambiguous)

  return results


# Print a prominent block listing any groups whose delivery is uncertain, so
# they are never silently forgotten. `ambiguous` is {chat_id: name}.
def _reportAmbiguous(ambiguous):
  if not ambiguous:
    return
  print(f"\n  {sand}{bold}⚠  {len(ambiguous)} group(s) with UNCERTAIN delivery — CHECK MANUALLY:{reset}")
  for chat_id, name in ambiguous.items():
    print(f"  {sand}  • {name} {stone}({chat_id}){reset}")
  print(f"  {stone}These timed out after the message was sent — it may or may not have arrived.{reset}")
  print(f"  {stone}Recorded as not-sent; re-sending may create a duplicate. Saved to {AMBIGUOUS_FILE}.{reset}")
