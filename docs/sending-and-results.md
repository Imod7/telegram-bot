# Sending & Results

## Running the script

1. Activate the virtual environment:
   ```bash
   source env-telegram-bot/bin/activate
   ```
2. Generate the Telegram message: `python3 format_message.py` (writes `files/out/telegram.html`).
3. Verify the target groups in `files/groups.txt` and the API key in `.env`.
4. Run:
   ```bash
   python3 main.py
   ```
5. The script will:
   - Preview the message and prompt for confirmation
   - Detect any previous run and offer to **resume** (see below)
   - List the recipient groups and prompt for confirmation
   - Send with progress updates (`[1/89] Sent to ...`)
   - Print a summary of successes, failures, and uncertain sends
   - Save results to `files/last_send_results.json`
   - Optionally prompt to update the Excel tracker
6. Verify delivery in the Telegram chats, then `deactivate`.

## Resume after an interruption

Results are saved to `files/last_send_results.json` **after every single send**, so an interruption
(Ctrl+C, crash, dropped connection) never loses progress.

On the next run, if a prior results file exists, the bot shows how many groups were already sent and
when the file was last updated, then asks what to do:

- **Resume** — skip the groups already sent successfully; send only the remaining ones
  (previously failed + never attempted). The saved record is preserved and extended.
- **Start fresh** — send to **all** groups and reset the record.
- **Cancel** — send nothing.

### Which to choose

| Situation | Choose |
|-----------|--------|
| Same message, a run was interrupted part-way | **Resume** |
| A brand-new message / new campaign | **Start fresh** |

> A completed campaign leaves every group marked sent. If you then start a **new** message, pick
> **Start fresh** — otherwise Resume would treat those groups as already done. Resume is only for
> finishing an interrupted run of the *same* message.

## Reliability: timeouts, retries & uncertain delivery

Each send uses a network timeout of **10s connect / 30s read**, so a bad connection can never hang
the whole run indefinitely.

- **Connect failure** (never reached Telegram) → the message was *not* delivered. Retried up to
  **3×**, then marked failed. Safe to re-send on the next Resume.
- **Read timeout** (request sent, no response came back) → delivery is **uncertain** — the message
  may or may not have arrived. This is **not** retried (a blind retry could duplicate it).

### Uncertain sends are flagged, not silently retried

Because Telegram's `sendMessage` has no idempotency key, a send that times out *after* the server
processed it can't be told apart from one that never arrived. When that happens the bot:

1. Records the group as **not sent** in `last_send_results.json` (conservative — Excel shows "No").
2. Adds it to `files/last_send_ambiguous.json`.
3. Prints a prominent `⚠ CHECK MANUALLY` block at the end listing each uncertain group.
4. On the next Resume, **holds these back** from the automatic re-send and lists them again, with an
   explicit opt-in prompt ("also re-send to the N uncertain group(s)? may duplicate").

So the only group that can ever be duplicated is one you consciously choose to re-send. Verify the
flagged chats in Telegram; a group is cleared from the uncertain list automatically once a later run
delivers to it cleanly.

## Updating Excel tracking (standalone)

To update the tracker independently of a send:

```bash
python3 update_excel.py
```

It will:

1. Load the most recent results (`files/last_send_results.json`).
2. Show which groups succeeded and which failed.
3. List the available columns from the sheet header row.
4. Prompt for a target column and write `Yes`/`No` accordingly.

The file used is `files/External Partners Channels.xlsx` (sheet `Channels`). It matches chat IDs from
column A against the send results and writes to the selected column. (A send run can also prompt to do
this at the end.)
