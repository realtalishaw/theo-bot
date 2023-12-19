# commands/onboarding.py

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# Define states for the ConversationHandler
EMAIL, PHONE, BIO, WATCH_VIDEO, QUIZ, APPROVAL = range(6)

# Start the conversation
def start_onboarding(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Welcome to the onboarding process. Please enter your email.")
    return EMAIL

# Handle email input
def email(update: Update, context: CallbackContext) -> int:
    print("email")
    user_email = update.message.text
    context.user_data['email'] = user_email
    update.message.reply_text("Thank you. Now, please enter your phone number.")
    return PHONE

# Handle phone input
def phone(update: Update, context: CallbackContext) -> int:
    user_phone = update.message.text
    context.user_data['phone'] = user_phone
    update.message.reply_text("Great! Lastly, please tell us something about yourself.")
    return BIO

# Handle bio input
def bio(update: Update, context: CallbackContext) -> int:
    user_bio = update.message.text
    context.user_data['bio'] = user_bio
    update.message.reply_text("Now, let's proceed to the onboarding videos.")
    # Trigger video watching process
    return WATCH_VIDEO

# Handle video watching process
def watch_video(update: Update, context: CallbackContext) -> int:
    # Assume the user watches the video
    update.message.reply_text("Please answer the following quiz based on the videos.")
    # Trigger quiz process
    return QUIZ

# Handle quiz process
def quiz(update: Update, context: CallbackContext) -> int:
    # Process quiz answers
    update.message.reply_text("Your answers have been submitted for review.")
    # Send data to the super_admin for approval
    return APPROVAL

# Handle quiz completion and notify super_admin
def approval(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    approval_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Approve", callback_data=f"approve_{update.message.from_user.id}")]
    ])
    
    # Notify the super_admin
    # Replace 'SUPER_ADMIN_CHAT_ID' with the actual chat ID of the super_admin
    context.bot.send_message(chat_id='SUPER_ADMIN_CHAT_ID',
                             text=f"New user {user_data['username']} has completed onboarding. Approve?",
                             reply_markup=approval_button)

    return ConversationHandler.END

# Cancel the conversation
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Onboarding process has been cancelled.')
    return ConversationHandler.END

# Setup ConversationHandler for onboarding
def setup_onboarding(dp):
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_onboarding)],
        states={
            EMAIL: [MessageHandler(Filters.text & ~Filters.command, email)],
            PHONE: [MessageHandler(Filters.text & ~Filters.command, phone)],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
            WATCH_VIDEO: [MessageHandler(Filters.text & ~Filters.command, watch_video)],
            QUIZ: [MessageHandler(Filters.text & ~Filters.command, quiz)],
            APPROVAL: [MessageHandler(Filters.text & ~Filters.command, approval)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)
