from gtts import gTTS
import os

def text_to_voice(text: str, language: str) -> str:
    """
    Converts text to a voice message file.
    Supports English, Arabic, and Hindi.
    Returns the path to the generated audio file.
    """

    # Map language names to gTTS language codes
    language_codes = {
        "English": "en",
        "Arabic": "ar",
        "Hindi": "hi"
    }

    # Get the language code — default to English
    lang_code = language_codes.get(language, "en")

    # Generate the voice file
    tts = gTTS(text=text, lang=lang_code, slow=False)

    # Save to a temp file
    audio_path = f"briefing_{lang_code}.mp3"
    tts.save(audio_path)

    return audio_path