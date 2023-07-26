import os
from dotenv import load_dotenv
import logging
from telegram import __version__ as TG_VER
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    filters,
    MessageHandler,
)

# Checking Version
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Importing environment variables
load_dotenv()
token = os.environ.get("token")


# Start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hello {user.mention_html()} Sir, I'm your personal assistant. "
    )


# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("For help click menu button")


# Mimic message handler
async def mimic_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mimic the user message."""
    await update.message.reply_text(update.message.text)


# Main function containd all handlers
def main() -> None:
    # Create the Application and pass it your bot's token
    application = Application.builder().token(token=token).build()

    # All message handler
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, mimic_message)
    )
    # All command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
