# 💬 BriefMe — WhatsApp AI Briefing Agent

> Stop scrolling through 200 messages every morning.  
> Get a 30-second AI briefing — in your language, in your voice.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Groq](https://img.shields.io/badge/Groq-LLaMA3.3-orange?style=flat-square)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?style=flat-square&logo=telegram)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?style=flat-square&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🔥 The Problem

Professionals in the UAE and GCC are part of **10+ WhatsApp groups**.  
Every morning they waste **20+minutes** scrolling through noise —  
good morning messages, memes, irrelevant updates —  
just to find **3 important things**.

There had to be a better way.

---

## 💡 The Solution

**BriefMe** is an AI agent that reads your WhatsApp chat export,  
understands what matters, and delivers a clean briefing —  
as text and as a voice message — in English, Arabic, or Hindi.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 AI Summarization | Extracts decisions, action items, urgent issues |
| 🌍 Multilingual | Briefings in English, Arabic, and Hindi |
| 🎤 Voice Message | Sends an audio briefing on Telegram |
| 📱 Telegram Bot | No app needed — works inside Telegram |
| 🖥️ Web App | Upload via browser with Streamlit |
| 🔒 Privacy First | Your chat never stored — processed and deleted |

---

## 🏗️ System Architecture

```
WhatsApp Export (.zip / .txt)
          │
          ▼
    📄 Parser Layer
    (Extracts messages, handles multilingual text,
     filters noise like media and system messages)
          │
          ▼
    🧠 AI Summarization Layer
    (Groq API — LLaMA 3.3 70B)
    (Extracts: Decisions / Actions / Questions / Urgent)
          │
          ▼
    🌍 Language Layer
    (English / Arabic / Hindi)
          │
          ├──────────────────┐
          ▼                  ▼
   📋 Text Briefing    🎤 Voice Message
   (Telegram / Web)   (gTTS → Telegram)
```

---

## 📁 Project Structure

```
BriefMe/
├── app.py              # Streamlit web interface
├── bot.py              # Telegram bot handler
├── parser.py           # WhatsApp chat parser
├── summarizer.py       # Groq AI summarization engine
├── tts.py              # Text to voice converter
├── voice.py            # Browser voice output
├── .env                # API keys (never committed)
├── requirements.txt    # Dependencies
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/RajitKrishna-ai/BriefMe
cd BriefMe
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API keys
Create a `.env` file:
```
GROQ_API_KEY=your_groq_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

### 4. Run the Web App
```bash
streamlit run app.py
```

### 5. Run the Telegram Bot
```bash
python bot.py
```

---

## 🤖 How to Use the Telegram Bot

1. Search your bot on Telegram
2. Type `/start`
3. Paste your WhatsApp chat messages
4. Type `/summarize`
5. Choose your language 🇬🇧 🇦🇪 🇮🇳
6. Receive your briefing as text + voice 🎤

---

## 🧠 AI Prompt Design

The AI is instructed to extract only what matters:

```
📌 KEY DECISIONS   — What was decided?
✅ ACTION ITEMS    — Who needs to do what?
❓ OPEN QUESTIONS  — What is still unresolved?
🔥 URGENT          — What needs immediate attention?
```

Supports mixed language chats — Hindi + English + Arabic in one chat — and always responds in the user's chosen language.

---

## ⚖️ Tradeoffs & Decisions

| Decision | Why |
|---|---|
| Groq over OpenAI | Free tier, faster inference, no credit card |
| LLaMA 3.3 70B | Best free model for multilingual understanding |
| gTTS over pyttsx3 | gTTS supports Arabic and Hindi, pyttsx3 doesn't |
| Telegram over WhatsApp | Official API, no restrictions, instant deployment |
| Streamlit for web | Fastest way to ship a clean UI in Python |

---

## 🔮 What's Next I will Building

- [ ] Auto-detect exported chats from a watched folder
- [ ] Daily scheduled briefings at 9am
- [ ] WhatsApp Business API integration
- [ ] Urgency scoring per message
- [ ] Summary history dashboard

---

## 👨‍💻 Built By

**Rajit R Krishna**  
Dubai-based Data Scientist & AI Engineer  
3+ years building ML, NLP, and Generative AI solutions  
across Banking, Aviation, Healthcare, and E-Commerce in UAE & GCC

---

## 📄 License

MIT License — free to use, modify, and distribute.
