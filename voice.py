import pyttsx3

def speak_summary(summary_text: str):
    """
    Converts the AI summary text to speech and plays it out loud.
    Uses pyttsx3 — works 100% offline, no API key needed.
    """

    # Initialize the text-tospeech engine
    engine = pyttsx3.init()

    # --- Voice Settings --
    engine.setProperty('rate', 165)      # Speed: 150=slow, 200=fast. 165 sounds natural perfect for my use case
    engine.setProperty('volume', 1.0)    # Volume: 0.0 to 1.0

    # Optional to chose: pick a voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # 0 = male, 1 = female

    print("🔊 Reading your briefing out loud...\n")

    # Speaking the summary
    engine.say(summary_text)

    # tp wait until speaking is fully done before continuing
    engine.runAndWait()

    print("✅ Done speaking!")


# ---- Quick Test ----
if __name__ == "__main__":
    from parser import parse_whatsapp_chat, format_for_ai
    from summarizer import summarize_chat

    # Load and parse the real chat i have loaded
    messages = parse_whatsapp_chat(r"WhatsApp Chat with Axora  Front office support.txt")
    formatted = format_for_ai(messages)

    print("🤖 Getting AI summary...\n")
    summary = summarize_chat(formatted)

    print("---- YOUR DAILY BRIEFING ----")
    print(summary)
    print("\n")

    # Now speak it out loud!
    speak_summary(summary)