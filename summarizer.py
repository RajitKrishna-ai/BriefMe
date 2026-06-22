import os
from groq import Groq
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()

# Initialize Groq client — to reads GROQ_API_KEY automatically from .env
client = Groq()

def summarize_chat(formatted_chat: str) -> str:
    """
    Sends the formatted WhatsApp chat to Groq AI and gets back
    a clean professional briefing with only what matters.
    Works with English, Hindi, Arabic, and mixed language chats.
    """

    # This is the instruction that i will give the AI
    system_prompt = """
You are a smart assistant that reads WhatsApp group chats and extracts what matters.

Your job is to produce a clean daily briefing with these sections:

1. 📌 KEY DECISIONS — What was decided?
2. ✅ ACTION ITEMS — Who needs to do what?
3. ❓ OPEN QUESTIONS — What is still unresolved?
4. 🔥 URGENT — Anything that needs immediate attention?

Rules:
- Be concise. No fluff, point to point.
- If messages are in Hindi or Arabic, still respond in English.
- Ignore greetings, media messages, and small talk.
- If nothing important was discussed, say "Nothing important to report."
"""

    # Send the chat to Groq and get a response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # Free, fast, and smart enough for this purpose
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the WhatsApp chat:\n\n{formatted_chat}"}
        ],
        temperature=0.3,   # Low temperature = more focused, less creative
        max_tokens=1000
    )

    # Extracting the text from the response
    return response.choices[0].message.content


# ---- Quick Testin ----
if __name__ == "__main__":
    from parser import parse_whatsapp_chat, format_for_ai

    # Use your real chat file
    messages = parse_whatsapp_chat(r"C:\Users\Rajit\Desktop\whatsapp-summarizer\WhatsApp Chat with Axora  Front office support.txt")
    formatted = format_for_ai(messages)

    print("🤖 Sending to Groq AI...\n")
    summary = summarize_chat(formatted)

    print("---- YOUR DAILY BRIEFING ----")
    print(summary)