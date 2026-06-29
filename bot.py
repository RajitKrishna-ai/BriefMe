import os
import logging
import subprocess
import sys
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)
from summarizer import summarize_chat_multilingual
subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv", "groq", "python-telegram-bot", "gtts"])

# ---- Load environment variables ----
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ---- Logging for debugging ----
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ---- Conversation states ----
WAITING_FOR_CHAT, WAITING_FOR_LANGUAGE = range(2)

# ---- Language options shown to user ----
LANGUAGE_KEYBOARD = [["🇬🇧 English", "🇦🇪 Arabic", "🇮🇳 Hindi"]]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /start command.
    Welcomes the user and tells them what to do.
    """
    await update.message.reply_text(
        "👋 Welcome to *BriefMe* — Your WhatsApp AI Briefing Agent!\n\n"
        "📋 Here's how it works:\n"
        "1️⃣ Paste or forward your WhatsApp chat messages here\n"
        "2️⃣ Type /summarize when done\n"
        "3️⃣ Choose your language\n"
        "4️⃣ Get your instant briefing!\n\n"
        "Start by pasting your chat messages 👇",
        parse_mode="Markdown"
    )
    # Clear any previous chat stored in memory
    context.user_data["chat_messages"] = []
    return WAITING_FOR_CHAT


async def collect_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Collects all messages the user pastes or forwards.
    Stores them in memory until user types /summarize.
    """
    # Initialize list if not exists
    if "chat_messages" not in context.user_data:
        context.user_data["chat_messages"] = []

    # Store each message with sender name
    sender = update.message.from_user.first_name
    text = update.message.text

    context.user_data["chat_messages"].append(f"{sender}: {text}")

    await update.message.reply_text(
        f"✅ Got it! Keep pasting more messages or type /summarize when ready."
    )
    return WAITING_FOR_CHAT


async def summarize_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Triggered when user types /summarize.
    Asks them to choose a language for the briefing.
    """
    messages = context.user_data.get("chat_messages", [])

    if not messages:
        await update.message.reply_text(
            "⚠️ No messages found! Please paste your WhatsApp chat first."
        )
        return WAITING_FOR_CHAT

    await update.message.reply_text(
        "🌍 Choose your briefing language:",
        reply_markup=ReplyKeyboardMarkup(
            LANGUAGE_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return WAITING_FOR_LANGUAGE


async def generate_briefing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Takes the chosen language, sends chat to Groq AI,
    replies with enhanced briefing (stats + urgency + senders) + voice message.
    """
    language_choice = update.message.text

    # Map button text to language name
    language_map = {
        "🇬🇧 English": "English",
        "🇦🇪 Arabic": "Arabic",
        "🇮🇳 Hindi": "Hindi",
        "english": "English",
        "arabic": "Arabic",
        "hindi": "Hindi",
    }
    language = language_map.get(language_choice, language_map.get(language_choice.lower(), "English"))

    await update.message.reply_text(
        f"🤖 Analysing your chat in {language}...",
        reply_markup=ReplyKeyboardRemove()
    )

    # Get stored messages and format them
    messages = context.user_data.get("chat_messages", [])
    formatted_chat = "\n".join(messages)

    # Send to Groq AI — enhanced summary
    summary = summarize_chat_multilingual(formatted_chat, language)

    # Get urgency score for emoji reaction
    from summarizer import get_urgency_score
    score = get_urgency_score(summary)

    # Pick emoji based on urgency
    if score >= 8:
        urgency_emoji = "🚨 HIGH URGENCY"
    elif score >= 5:
        urgency_emoji = "⚠️ MEDIUM URGENCY"
    else:
        urgency_emoji = "✅ LOW URGENCY"

    # Reply with full briefing
    await update.message.reply_text(
        f"📋 *BriefMe Daily Briefing*\n"
        f"_{urgency_emoji}_\n\n"
        f"{summary}",
        parse_mode="Markdown"
    )

    # Generate and send voice message
    await update.message.reply_text("🎤 Generating voice message...")

    try:
        from tts import text_to_voice

        # Convert summary to voice in chosen language
        audio_path = text_to_voice(summary, language)

        # Send voice message to Telegram
        with open(audio_path, "rb") as audio:
            await update.message.reply_voice(voice=audio)

        # Clean up audio file after sending
        os.remove(audio_path)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Voice generation failed: {str(e)}")

    # Clear messages for next session
    context.user_data["chat_messages"] = []

    await update.message.reply_text(
        "✅ Done! Paste new messages anytime to start again.\n"
        "Type /start to begin a new session."
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels the current session."""
    context.user_data["chat_messages"] = []
    await update.message.reply_text("❌ Session cancelled. Type /start to begin again.")
    return ConversationHandler.END


def main():
    """Starts the Telegram bot."""
    print("🤖 BriefMe Bot is running...")

    # Build the bot application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Conversation flow handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_FOR_CHAT: [
                CommandHandler("summarize", summarize_command),
                MessageHandler(filters.TEXT & ~filters.COMMAND, collect_messages)
            ],
            WAITING_FOR_LANGUAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, generate_briefing)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv_handler)

    # Start polling for messages
    app.run_polling()


if __name__ == "__main__":
    main()