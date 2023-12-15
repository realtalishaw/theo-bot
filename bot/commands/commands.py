from telegram import Update
from telegram.ext import CallbackContext

# Command handler for the /start command
def start(update: Update, context: CallbackContext) -> None:
    # Get the first name of the user from the update object
    first_name = update.message.chat.first_name

    # Create a greeting message
    greeting_message = f"Hello {first_name}! Welcome to TheoBot. How can I assist you today?"

    # Send the greeting message to the user
    update.message.reply_text(greeting_message)
