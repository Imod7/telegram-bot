# Recipient Groups

The bot sends **only** to the groups listed in `files/groups.txt`.

## Format

One group per line:

```
-TelegramChatID, TelegramChatName
```

Example:

```
-123456789, MyGroupChat
-1009876543210, Example Exchange Tech
```

Add each target group on its own line. A `files/groups-test.txt` with just your test chats is kept
alongside it — copy it over `files/groups.txt` when you want a safe test run:

```bash
cp files/groups-test.txt files/groups.txt   # test only
```

## Adding the bot to a new group chat

If the bot needs to reach a group not yet in `groups.txt`:

1. Add the bot to the Telegram group as you would any other member.
2. Retrieve the group's chat ID by opening this URL in your browser:
   ```
   https://api.telegram.org/bot<YourBOTToken>/getUpdates
   ```
3. Find the group name in the JSON response and copy its chat ID.
4. Add the `chatID, name` line to `files/groups.txt`.

> **Note:** `getUpdates` sometimes returns an empty response right after a bot is added to a new
> group. Workaround: remove the bot from an existing group and re-add it — this refreshes the
> endpoint so all chat IDs appear, including the new one.
