# Message Formatting (Multi-Channel)

You write the message **once** in `files/message.md` (Markdown), then `format_message.py`
renders it into the four dialects used across channels — so the same announcement can go to
Telegram, Element, Slack, and email without re-formatting by hand.

## 1. Write the source

Edit `files/message.md` using standard Markdown:

- `# Title` — title (becomes the email **Subject**; bold in chat channels)
- `## Section` — section header
- `**bold**`, `*italic*` / `_italic_`
- `[label](url)` — link
- `- item` — bullet
- `` `inline code` `` — monospace
- ```` ``` ```` fenced block — code block, kept verbatim
- blank line — paragraph break

## 2. Generate the per-channel formats

No virtualenv needed — the formatter uses only the Python standard library:

```bash
python3 format_message.py
```

It writes one file per channel to `files/out/`:

| File | Channel | Format |
|------|---------|--------|
| `telegram.html` | Telegram | HTML subset (`<b>`, `<i>`, `<a>`, `<code>`, `<pre>`, `•` bullets) |
| `element.md` | Element / Matrix | Markdown |
| `slack.txt` | Slack | mrkdwn (`*bold*`, `<url\|label>`, `•` bullets) |
| `email.txt` | Email | Plain text (Subject line, greeting, sign-off) |

The bot (`main.py`) reads `files/out/telegram.html` directly, so **no extra step is needed for
Telegram**. Copy-paste `element.md`, `slack.txt`, and `email.txt` into their respective channels.

> **Regenerate after every edit.** If you change `message.md` you must re-run
> `python3 format_message.py`, or the bot will send the previous version.

**Notes**
- Reserved characters (`&`, `<`, `>`) are escaped automatically for Telegram and Slack; links are preserved intact.
- Code is never re-formatted: text inside `` ` `` or a ``` ``` ``` fence keeps its `_underscores_` and
  `*stars*` verbatim instead of being read as emphasis. Telegram gets `<code>` / `<pre>`, Element and
  Slack keep the fences, and email drops the markers.
- The email greeting and sign-off are editable constants (`EMAIL_GREETING`, `EMAIL_SIGNOFF`) at the top of `format_message.py`; they appear only in the email output and never leak into the chat formats.

## Telegram HTML details (only if you hand-edit `telegram.html`)

The Telegram output uses the [Telegram Bot API HTML style](https://core.telegram.org/bots/api#html-style).
If you edit `files/out/telegram.html` directly instead of regenerating it:

**Supported tags:** `<b>`/`<strong>`, `<i>`/`<em>`, `<u>`/`<ins>`, `<s>`/`<strike>`/`<del>`,
`<code>`, `<pre>`, `<a href="...">`, `<blockquote>`.

**Not supported:** `<ul>`, `<li>`, `<br>`, `<p>` — these cause a send error. Use plain-text bullet
characters (`•`, `-`) instead. (The formatter handles all of this for you.)

## Pre-send verification

1. Always send to a **test group first** (put only your test group in `files/groups.txt`) to verify
   formatting before broadcasting to everyone — see [Recipient Groups](./recipients.md).
2. If a message is truncated or fails to send, inspect `files/out/telegram.html` for special
   characters (such as `&`) that conflict with HTML parsing. The formatter escapes these
   automatically; if you hand-edited the file, replace `&` with `&amp;` and remove any unsupported tags.
