from telegram.ext import Updater, CommandHandler
import logging
from commands.commands import start  # Import the start command handler

# Set up basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# Error Handler
def error(update, context):
    # Log errors caused by Updates.
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Main function where the bot is initialized
def main():
    # Create Updater object and attach dispatcher to it
    updater = Updater("6858884073:AAH_3MgTf9k1v8VKAKxCZqliday9cTW4X14", use_context=True)
    dp = updater.dispatcher

    # Add handlers for commands by importing them from commands.py
    dp.add_handler(CommandHandler("start", start))
    
    # Add an error handler
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
