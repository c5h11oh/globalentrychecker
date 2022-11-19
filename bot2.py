import asyncio
import logging
import ge_checker
import json
from telegram import Bot, ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from threading import Thread
from time import sleep

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def bot() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(secrets["token"]).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

async def check_async():
    check_bot = Bot(secrets["token"])
    async with check_bot:
        while True:
            result = ['hello', 'I\'m bot2'] #ge_checker.check_availability(preferences)
            await check_bot.send_message(chat_id=secrets["authorized_id"][0], text=str(result[1]))
            sleep(5)

def check():
    asyncio.run(check_async())

if __name__ == "__main__":
    with open('secrets.json', 'r') as sfile, open('preferences.json', 'r') as pfile:
        secrets = json.load(sfile)
        preferences = json.load(pfile)
    Thread(target=bot).start()
    Thread(target=check).start()