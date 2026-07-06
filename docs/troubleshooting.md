# Troubleshooting & Maintenance

## Troubleshooting

- **Truncated or unsent messages** — Special characters in `files/out/telegram.html` may interfere
  with HTML parsing. The formatter escapes `&`, `<`, `>` automatically; if you hand-edited the file,
  replace `&` with `&amp;` and remove any unsupported tags (`<ul>`, `<li>`, `<br>`, `<p>`). Use
  plain-text bullet characters instead.
- **`ModuleNotFoundError: No module named 'requests'`** — The virtual environment isn't activated.
  Run `source env-telegram-bot/bin/activate` first.
- **Message not delivered to a specific group** — Verify the chat ID at
  `https://api.telegram.org/bot<YourBOTToken>/getUpdates`. If wrong, fix it in `files/groups.txt`.
- **A run got stuck for a long time** — Older versions had no network timeout; the current version
  times out (10s connect / 30s read) and moves on. If a group shows `TIMEOUT — delivery UNCERTAIN`,
  see [Reliability](./sending-and-results.md#reliability-timeouts-retries--uncertain-delivery).
- **The next run wants to send to everyone again** — The results file reflects the *last* run. For a
  new message, that's expected — choose **Start fresh**. For finishing an interrupted run, choose
  **Resume**. See [Resume](./sending-and-results.md#resume-after-an-interruption).

## Maintenance

Keep dependencies current:

```bash
pip list --outdated                 # check for outdated packages
pip install --upgrade <package>     # upgrade one
pip freeze > requirements.txt       # record current versions
```
