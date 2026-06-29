import os
from groq import Groq
# from dotenv import load_dotenv

# Load the API key from .env file
# load_dotenv()

# Initialize Groq client
# client = Groq()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))



def summarize_chat(formatted_chat: str) -> str:
    """
    Basic summarization for the Streamlit web app.
    """
    system_prompt = """
You are a smart assistant that reads WhatsApp group chats and extracts what matters.

Your job is to produce a clean daily briefing with these sections:

1.  KEY DECISIONS — What was decided?
2.  ACTION ITEMS — Who needs to do what? (mention sender names)
3.  OPEN QUESTIONS — What is still unresolved?
4.  URGENT — Anything that needs immediate attention?

Rules:
- Be concise. No fluff.
- Always mention WHO is responsible for each action item.
- If messages are in Hindi or Arabic, still respond in English.
- Ignore greetings, media messages, and small talk.
- If nothing important was discussed, say "Nothing important to report."
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the WhatsApp chat:\n\n{formatted_chat}"}
        ],
        temperature=0.3,
        max_tokens=1000
    )
    return response.choices[0].message.content


def summarize_chat_multilingual(formatted_chat: str, language: str) -> str:
    """
    Advanced summarization for Telegram bot.
    Includes: sender names, urgency score, time range, message count.
    Responds in the chosen language.
    """

    system_prompt = f"""
You are a smart assistant that reads WhatsApp group chats and extracts what matters.
Respond ONLY in {language}.

Your briefing must follow this EXACT format:

📊 CHAT STATS
- Messages analysed: [count the messages]
- Active senders: [list unique sender names]
- Time span: [first timestamp → last timestamp]

🔥 URGENCY SCORE: [X/10]
[One line explaining why — e.g. "3 unresolved issues detected"]

📌 KEY DECISIONS
- [Decision 1]
- [Decision 2]

✅ ACTION ITEMS
- [Sender Name]: [what they need to do]
- [Sender Name]: [what they need to do]

❓ OPEN QUESTIONS
- [Question 1]
- [Question 2]

🚨 URGENT
- [Urgent item 1]
- [Urgent item 2]

Rules:
- Always mention sender names in action items.
- Urgency score: 1=nothing urgent, 10=critical issues unresolved.
- Ignore greetings, good mornings, and small talk.
- If nothing important, say so clearly.
- Be concise. No fluff.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the WhatsApp chat:\n\n{formatted_chat}"}
        ],
        temperature=0.3,
        max_tokens=1500
    )
    return response.choices[0].message.content


def get_urgency_score(summary: str) -> int:
    """
    Extracts the urgency score number from the summary text.
    Returns a number between 1-10.
    """
    try:
        # Look for pattern like "URGENCY SCORE: 8/10"
        import re
        match = re.search(r'URGENCY SCORE[:\s]+(\d+)', summary, re.IGNORECASE)
        if match:
            return int(match.group(1))
    except:
        pass
    return 0