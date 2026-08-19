"""
Render one Markdown source message into every channel's dialect.

Write the message once in files/message.md (standard Markdown), then run:

    python3 format_message.py

Outputs (files/out/):
  telegram.html  - Telegram HTML subset (<b>, <i>, <a>, bullets)
  element.md     - Markdown for Element / Matrix
  slack.txt      - Slack mrkdwn (*bold*, <url|label>, bullets)
  email.txt      - Plain-text email (Subject line + greeting + signoff)

The bot (main.py) reads files/out/telegram.html directly.

Supported source syntax:
  # Title            -> bold title (email: becomes the Subject line)
  ## Section         -> bold section header (email: UPPERCASE line)
  - item             -> bullet
  **bold**  *italic*  _italic_
  [label](url)
  `inline code`      -> monospace, never re-formatted
  ``` fenced block   -> code block, kept verbatim (Telegram <pre>)
  blank line         -> paragraph break
"""

import os
import re
import html

try:
    from src.colors import bold, slate, sage, stone, teal, reset, LINE, DOUBLE_LINE
except Exception:  # colors are cosmetic; fall back to no-ops
    bold = slate = sage = stone = teal = reset = ""
    LINE = "-" * 60
    DOUBLE_LINE = "=" * 60

SRC = "files/message.md"
OUT_DIR = "files/out"

# Email-only boilerplate (edit to taste; never leaks into chat formats)
EMAIL_GREETING = "Hi all,"
EMAIL_SIGNOFF = "Best regards,\nThe Polkadot Team"

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
ITALIC_STAR_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
ITALIC_US_RE = re.compile(r"_([^_]+)_")
CODE_RE = re.compile(r"`([^`]+)`")
FENCE_RE = re.compile(r"^```\s*(\S*)\s*$")

TARGETS = {
    # name: (output filename, target key)
    "telegram": ("telegram.html", "telegram"),
    "element": ("element.md", "element"),
    "slack": ("slack.txt", "slack"),
    "email": ("email.txt", "email"),
}


def _wrap(inner, kind, target):
    """Wrap already-inline-rendered text in bold ('b') or italic ('i')."""
    if target == "telegram":
        return f"<{kind}>{inner}</{kind}>"
    if target == "slack":
        return f"*{inner}*" if kind == "b" else f"_{inner}_"
    if target == "email":
        return inner  # plain text: drop emphasis markers
    return f"**{inner}**" if kind == "b" else f"*{inner}*"  # element / markdown


def _inline(text, target):
    """Render inline markup (links, bold, italic) for a target, escaping
    special characters where the target needs it (Telegram HTML / Slack)."""
    # 1. Stash inline code first: its contents are verbatim, so no escaping,
    #    emphasis or link rendering may touch them (shell snippets are full of
    #    _underscores_ and *stars* that are not markup).
    codes = []

    def stash_code(m):
        codes.append(m.group(1))
        return f"\x00CODE{len(codes) - 1}\x00"

    text = CODE_RE.sub(stash_code, text)

    # 2. Stash links so their URLs are not touched by escaping or emphasis.
    links = []

    def stash(m):
        links.append((m.group(1), m.group(2)))
        return f"\x00LINK{len(links) - 1}\x00"

    text = LINK_RE.sub(stash, text)

    # 3. Escape reserved characters.
    if target == "telegram":
        text = html.escape(text, quote=False)  # & < >
    elif target == "slack":
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # 4. Emphasis (bold before italic so ** is consumed first).
    text = BOLD_RE.sub(lambda m: _wrap(m.group(1), "b", target), text)
    text = ITALIC_STAR_RE.sub(lambda m: _wrap(m.group(1), "i", target), text)
    text = ITALIC_US_RE.sub(lambda m: _wrap(m.group(1), "i", target), text)

    # 5. Reinsert links, then code spans, rendered per target.
    def render_link(label, url):
        if target == "telegram":
            return f'<a href="{html.escape(url, quote=True)}">{html.escape(label, quote=False)}</a>'
        if target == "slack":
            # Paste-friendly: the <url|label> mrkdwn form only renders when a
            # message is posted via the Slack API, not when pasted into the
            # composer. A bare URL is the only thing Slack auto-links on paste,
            # so keep the label as plain text and leave the URL bare (no parens,
            # which can suppress auto-linking).
            return f"{label} {url}" if label != url else url
        if target == "email":
            return f"{label} ({url})"
        return f"[{label}]({url})"  # element / markdown

    for i, (label, url) in enumerate(links):
        text = text.replace(f"\x00LINK{i}\x00", render_link(label, url))
    for i, code in enumerate(codes):
        text = text.replace(f"\x00CODE{i}\x00", _code_span(code, target))
    return text


def _code_span(code, target):
    """Render `inline code`. Only Telegram needs escaping (it parses HTML);
    the other outputs are pasted by hand, where escapes would show literally."""
    if target == "telegram":
        return f"<code>{html.escape(code, quote=False)}</code>"
    if target == "email":
        return code  # plain text: drop the markers
    return f"`{code}`"  # element / slack


def _code_block(lines, lang, target):
    """Render a ``` fenced block. Contents are never re-formatted."""
    body = "\n".join(lines)
    if target == "telegram":
        escaped = html.escape(body, quote=False)
        if lang:
            return f'<pre><code class="language-{html.escape(lang, quote=True)}">{escaped}</code></pre>'
        return f"<pre>{escaped}</pre>"
    if target == "email":
        return body  # plain text: fences would just be noise
    if target == "slack":
        return f"```\n{body}\n```"
    return f"```{lang}\n{body}\n```"  # element / markdown


def _header(text, target):
    """Render a # or ## heading. Both become bold in chat targets."""
    inner = _inline(text, target)
    if target == "telegram":
        return f"<b>{inner}</b>"
    if target == "slack":
        return f"*{inner}*"
    if target == "email":
        return inner.upper()
    return f"**{inner}**"  # element / markdown


def _bullet(item, target):
    inner = _inline(item, target)
    return f"• {inner}" if target in ("telegram", "slack") else f"- {inner}"


def convert(source, target):
    """Render the full Markdown source into one target dialect."""
    subject = None
    out = []
    code_lines = None  # non-None while inside a ``` fence
    code_lang = ""
    for raw in source.splitlines():
        s = raw.strip()

        fence = FENCE_RE.match(s)
        if code_lines is not None:
            if fence:
                out.append(_code_block(code_lines, code_lang, target))
                code_lines = None
                code_lang = ""
            else:
                code_lines.append(raw.rstrip())  # keep indentation verbatim
            continue
        if fence:
            code_lines = []
            code_lang = fence.group(1)
            continue

        if not s:
            out.append("")
            continue
        if s.startswith("# "):
            title = s[2:].strip()
            if subject is None:
                subject = title
            if target == "email":
                continue  # H1 becomes the Subject line, not body
            out.append(_header(title, target))
        elif s.startswith("## "):
            out.append(_header(s[3:].strip(), target))
        elif s.startswith("- "):
            out.append(_bullet(s[2:].strip(), target))
        else:
            out.append(_inline(s, target))

    if code_lines is not None:  # unterminated fence: emit what we have
        out.append(_code_block(code_lines, code_lang, target))

    body = "\n".join(out).strip("\n")

    if target == "email":
        subj = subject or "Announcement"
        body = "\n".join(
            [f"Subject: {subj}", "", EMAIL_GREETING, "", body, "", EMAIL_SIGNOFF]
        )
    return body + "\n"


def main():
    print(f"\n{DOUBLE_LINE}")
    print(f"  {bold}{slate}Message Formatter{reset}")
    print(DOUBLE_LINE)

    if not os.path.exists(SRC):
        print(f"\n  Source not found: {SRC}")
        print(f"  Write your message there in Markdown, then re-run.\n")
        return

    with open(SRC, encoding="utf-8") as f:
        source = f.read()

    os.makedirs(OUT_DIR, exist_ok=True)

    for name, (fname, target) in TARGETS.items():
        rendered = convert(source, target)
        path = os.path.join(OUT_DIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"  {sage}  {name:<9}{reset} -> {stone}{path}{reset}")

    print(f"\n{DOUBLE_LINE}")
    print(f"  {bold}{sage}Done. 4 formats generated from {SRC}.{reset}")
    print(DOUBLE_LINE)
    print(f"  {stone}Telegram: sent by main.py (reads out/telegram.html)  |  Element / Slack / Email: copy-paste from files/out/{reset}\n")


if __name__ == "__main__":
    main()
