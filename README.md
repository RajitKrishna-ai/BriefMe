# 💬 WhatsApp AI Briefing Agent

> Stop scrolling through 200 messages every morning. Get a 30-second AI briefing instead.

## 🔥 What it does
- Upload any WhatsApp group chat export (.zip or .txt)
- AI reads every message and extracts only what matters
- Get a clean briefing: decisions, action items, urgent issues
- Hear it read out loud in your browser

## 🧠 Tech Stack
- **Groq API** (LLaMA 3.3) — AI summarization
- **Python** — parsing & backend logic
- **Streamlit** — web interface
- **Web Speech API** — browser voice output

## 🚀 Run Locally

1. Clone the repo
   git clone https://github.com/YOURUSERNAME/whatsapp-summarizer

2. Install dependencies
   pip install -r requirements.txt

3. Add your Groq API key
   Create a .env file:
   GROQ_API_KEY=your_key_here

4. Run the app
   streamlit run app.py

## 📁 Project Structure
whatsapp-summarizer/
├── app.py          # Streamlit web UI
├── parser.py       # WhatsApp chat parser
├── summarizer.py   # Groq AI summarization
├── voice.py        # Voice output
├── requirements.txt
└── README.md