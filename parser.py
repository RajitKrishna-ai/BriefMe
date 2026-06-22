import re

def parse_whatsapp_chat(file_path):
    """
    Reads a WhatsApp exported .txt file or zip file or pdf and returns a clean list of messages.
    Supports: contact names, +971 / +91 numbers, Hindi, Arabic, Emoji.
    Format: DD/MM/YY, HH:MM am/pm - Sender: Message
    """

    messages = []

    # Matches: "15/05/26, 10:58 am - Sender Name: message text"
    # Also matches: "15/05/26, 6:17 pm - +971 52 984 6811: message text"
    pattern = re.compile(
        r'(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}\s[apm]{2})\s-\s([^:]+):\s(.+)',
        re.IGNORECASE
    )

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            match = pattern.match(line)

            if match:
                date, time, sender, message = match.groups()

                # Skip media-only messages — nothing to summarize
                if "<media omitted>" in message.lower():
                    continue

                # Skip system/encryption notices
                if "end-to-end" in message.lower():
                    continue

                messages.append({
                    "date": date,
                    "time": time,
                    "sender": sender.strip(),
                    "message": message.strip()
                })

    return messages


def format_for_ai(messages):
    """
    Converts parsed messages into a clean readable block for the AI.
    Work with English, Hindi, Arabic, and mixed language chats.
    """

    if not messages:
        return "No messages found / Empty file."

    formatted = []
    for msg in messages:
        formatted.append(f"[{msg['date']} {msg['time']}] {msg['sender']}: {msg['message']}")

    return "\n".join(formatted)


# ---- Quick Test ----
if __name__ == "__main__":
    import sys

    file = "sample_chat.txt"

    # Usins a sample matching my exact WhatsApp format
    sample = """15/05/26, 6:20 pm - +91 81579 92207: Portal is taking long time to load
15/05/26, 6:58 pm - +971 50 257 3483: It's resolved, can you recheck
15/05/26, 7:02 pm - Sahal Shelu DXB: Still its not working properly
15/05/26, 7:13 pm - Shahid Clinic DXB: Now working
15/05/26, 7:32 pm - +971 50 257 3483: Thanks for the update 👍"""

    with open(file, "w", encoding="utf-8") as f:
        f.write(sample)

    messages = parse_whatsapp_chat(file)
    formatted = format_for_ai(messages)

    print(f"✅ Parsed {len(messages)} messages\n")
    print("---- Formatted Output ----")
    print(formatted)