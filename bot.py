import os
import sys
import logging
import subprocess

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)
from summarizer import summarize_chat_multilingual, get_urgency_score

# ---- Get token directly from environment (Railway injects this) ----
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# ---- Logging ----
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ---- Conversation states ----
WAITING_FOR_CHAT, WAITING_FOR_LANGUAGE = range(2)

# ---- Language keyboard ----
LANGUAGE_KEYBOARD = [["English", "Arabic", "Hindi"]]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /start command. Welcomes the user."""
    await update.message.reply_text(
        "Welcome to BriefMe - Your WhatsApp AI Briefing Agent!\n\n"
        "Here is how it works:\n"
        "1. Paste your WhatsApp chat messages here\n"
        "2. Type /summarize when done\n"
        "3. Choose your language\n"
        "4. Get your instant briefing!\n\n"
        "Start by pasting your chat messages below.",
        parse_mode="Markdown"
    )
    context.user_data["chat_messages"] = []
    return WAITING_FOR_CHAT


async def collect_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Collects all messages the user pastes."""
    if "chat_messages" not in context.user_data:
        context.user_data["chat_messages"] = []

    sender = update.message.from_user.first_name
    text = update.message.text
    context.user_data["chat_messages"].append(f"{sender}: {text}")

    await update.message.reply_text(
        "Got it! Keep pasting more messages or type /summarize when ready."
    )
    return WAITING_FOR_CHAT


async def summarize_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Triggered when user types /summarize."""
    messages = context.user_data.get("chat_messages", [])

    if not messages:
        await update.message.reply_text(
            "No messages found! Please paste your WhatsApp chat first."
        )
        return WAITING_FOR_CHAT

    await update.message.reply_text(
        "Choose your briefing language:",
        reply_markup=ReplyKeyboardMarkup(
            LANGUAGE_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return WAITING_FOR_LANGUAGE


async def generate_briefing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generates AI briefing and sends voice message."""
    language_choice = update.message.text

    language_map = {
        "English": "English",
        "Arabic": "Arabic",
        "Hindi": "Hindi",
    }
    language = language_map.get(language_choice, "English")

    await update.message.reply_text(
        f"Analysing your chat in {language}...",
        reply_markup=ReplyKeyboardRemove()
    )

    # Get stored messages
    messages = context.user_data.get("chat_messages", [])
    formatted_chat = "\n".join(messages)

    # Send to Groq AI
    summary = summarize_chat_multilingual(formatted_chat, language)

    # Get urgency score
    score = get_urgency_score(summary)
    if score >= 8:
        urgency_label = "HIGH URGENCY"
    elif score >= 5:
        urgency_label = "MEDIUM URGENCY"
    else:
        urgency_label = "LOW URGENCY"

    # Send text briefing
    await update.message.reply_text(
        f"BriefMe Daily Briefing\n"
        f"{urgency_label}\n\n"
        f"{summary}",
        parse_mode="Markdown"
    )

    # Generate and send voice message
    await update.message.reply_text("Generating voice message...")

    try:
        from tts import text_to_voice
        audio_path = text_to_voice(summary, language)
        with open(audio_path, "rb") as audio:
            await update.message.reply_voice(voice=audio)
        os.remove(audio_path)

    except Exception as e:
        await update.message.reply_text(f"Voice generation failed: {str(e)}")

    # Clear for next session
    context.user_data["chat_messages"] = []
    await update.message.reply_text(
        "Done! Paste new messages anytime.\n"
        "Type /start to begin a new session."
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels current session."""
    context.user_data["chat_messages"] = []
    await update.message.reply_text("Session cancelled. Type /start to begin again.")
    return ConversationHandler.END


def main():
    """Starts the Telegram bot."""
    print("BriefMe Bot is running...")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

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
    app.run_polling()


if __name__ == "__main__":
    main()
