from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler, CallbackContext
from utils.redis_cache import get_from_cache, set_in_cache
from utils.helper_functions import is_user_allowed
import re
from api.user import create_user

# Define states for the conversation
EMAIL, PHONE, BIO, ONBOARDING, WATCH_VIDEO, QUIZ = range(6)

# Define quiz questions and answers
quiz_questions = [
    ("Bevis Intro One Question Answer 4?", ["4", "22"], "4"),
    ("Bevis Intro 2 question answer idk:", ["Trump", "Biden", "IDK"], "IDK"),
    ("Bevis Key Featrures 2 anser Yup", ["No", "No", "Yup"], "Yup"),
    ("Bevis & PYramid 1_2 answer blue", ["Pink", "Orange", "Blue"], "Blue")
]
video_links = [
    "https://www.youtube.com/watch?v=3D10hw1lTUI",
    "https://www.youtube.com/watch?v=J5exx4q2skY",
    "https://www.youtube.com/watch?v=K8hkr3zWNB0",
    "https://www.youtube.com/watch?v=G5sLGDKFacc"
]
# Define the callback data for the buttons
BEGIN_ONBOARDING_CALLBACK_DATA = 'begin_onboarding'

# Email validation regex
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def start(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    user_first_name = update.message.from_user.first_name
    user_last_name = update.message.from_user.last_name
    user_username = update.message.from_user.username or "N/A"

    context.user_data['user_id'] = user_id
    context.user_data['first_name'] = user_first_name
    context.user_data['last_name'] = user_last_name
    context.user_data['username'] = user_username

    user_data = get_from_cache(str(user_id))
    
    if user_data is None:
        update.message.reply_text(f'Welcome {user_first_name}! Please enter your email:')
        return EMAIL
    elif user_data == 'unconfirmed':
        update.message.reply_text("Your registration is pending approval. You cannot access the bot at this moment.")
    else:
        update.message.reply_text('Welcome back to TheoBot! Type /help for a list of commands.')

    return EMAIL  # Assuming EMAIL is the next state



def collect_email(update: Update, context: CallbackContext) -> int:
    email = update.message.text
    if re.fullmatch(EMAIL_REGEX, email):
        context.user_data['email'] = email
        update.message.reply_text('Great! Now, please send me your phone number.')
        return PHONE
    else:
        update.message.reply_text('Invalid email. Please enter a valid email address:')
        return EMAIL

def collect_phone(update: Update, context: CallbackContext) -> int:
    phone = update.message.text
    if phone.isdigit() and 7 <= len(phone) <= 15:  # Basic validation for phone number
        context.user_data['phone'] = phone
        update.message.reply_text('Thanks! Lastly, tell me a bit about yourself.')
        return BIO
    else:
        update.message.reply_text('Invalid phone number. Please enter a valid phone number:')
        return PHONE

def collect_bio(update: Update, context: CallbackContext) -> int:
    bio = update.message.text
    context.user_data['bio'] = bio
    update.message.reply_text('Registration info collected.')
    
    # Add a "Begin" button to start the onboarding process
    keyboard = [[InlineKeyboardButton("Begin", callback_data=BEGIN_ONBOARDING_CALLBACK_DATA)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Click "Begin" to start the onboarding process:', reply_markup=reply_markup)
    return ONBOARDING

def start_onboarding(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    context.user_data['video_index'] = 0
    return send_video_message(update, context)

def send_video_message(update: Update, context: CallbackContext) -> int:
    video_index = context.user_data.get('video_index', 0)
    if video_index < len(video_links):
        # Send the video link
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Please watch this video: {video_links[video_index]}")
        # After sending the video, add a button to proceed to the quiz
        keyboard = [[InlineKeyboardButton("I've watched the video, proceed to the quiz", callback_data='proceed_to_quiz')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Click the button when you're ready to proceed to the quiz.", reply_markup=reply_markup)
        return WATCH_VIDEO
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Congratulations, you've completed all the videos and quizzes!")
        return end_onboarding(update, context)

def proceed_to_quiz_handler(update: Update, context: CallbackContext) -> int:
    return send_quiz_question(update, context)

def send_quiz_question(update: Update, context: CallbackContext) -> int:
    video_index = context.user_data.get('video_index', 0)
    question, options, _ = quiz_questions[video_index]
    keyboard = [[InlineKeyboardButton(option, callback_data=option)] for option in options]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text=question, reply_markup=reply_markup)
    return QUIZ

def quiz(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    video_index = context.user_data.get('video_index', 0)
    _, _, correct_answer = quiz_questions[video_index]
    if query.data == correct_answer:
        context.user_data['video_index'] += 1
        context.bot.send_message(chat_id=update.effective_chat.id, text="Correct! On to the next video.")
        return send_video_message(update, context)
    else:
        return send_quiz_question(update, context)

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Onboarding has been canceled.')
    return ConversationHandler.END

def end_onboarding(update: Update, context: CallbackContext) -> int:
    user_info = {
        "first_name": context.user_data.get('first_name'),
        "last_name": context.user_data.get('last_name'),
        "email": context.user_data.get('email'),
        "phone": context.user_data.get('phone'),
        "bio": context.user_data.get('bio'),
        "status": "PENDING"
    }

    create_user(user_info)  # Your API call

    context.bot.send_message(chat_id=update.effective_chat.id, text="Your onboarding and registration are complete and have been sent for approval.")

    admin_chat_id = '5915765775'  # Admin chat ID
    keyboard = [
        [InlineKeyboardButton("Approve", callback_data=f"approve_{context.user_data['user_id']}")],
        [InlineKeyboardButton("Deny", callback_data=f"deny_{context.user_data['user_id']}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    admin_message = f"New user registration for approval:\nFirst Name: {user_info['first_name']}\nLast Name: {user_info['last_name']}\nUsername: {context.user_data['username']}"
    context.bot.send_message(chat_id=admin_chat_id, text=admin_message, reply_markup=reply_markup)

    return ConversationHandler.END



def admin_approval_handler(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    
    # Parse the callback data to get the user_id and action
    user_id, action = query.data.split('_')
    
    if action == "approve":
        # Admin selects a planet, moon, and satellite for the user
        # This is a placeholder, you'll need to implement the actual logic
        #assign_planet_moon_satellite_to_user(user_id)
        
        # Make an API call to the verify user endpoint to approve the user
        #verify_user(user_id, True)  # Assuming this function takes user_id and a boolean for approval
        
        # Notify the user of their acceptance
        context.bot.send_message(chat_id=user_id, text="Congratulations, your registration has been approved!")
    elif action == "deny":
        # Make an API call to the verify user endpoint to deny the user
        #verify_user(user_id, False)  # Assuming this function takes user_id and a boolean for approval
        
        # Notify the user of their rejection
        context.bot.send_message(chat_id=user_id, text="Your registration has been denied.")
    
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        EMAIL: [MessageHandler(Filters.text & ~Filters.command, collect_email)],
        PHONE: [MessageHandler(Filters.text & ~Filters.command, collect_phone)],
        BIO: [MessageHandler(Filters.text & ~Filters.command, collect_bio)],
        ONBOARDING: [CallbackQueryHandler(start_onboarding, pattern=BEGIN_ONBOARDING_CALLBACK_DATA)],
        WATCH_VIDEO: [CallbackQueryHandler(proceed_to_quiz_handler, pattern='proceed_to_quiz')],
        QUIZ: [CallbackQueryHandler(quiz)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)



def help(update, context):
    if not is_user_allowed(update, context):
        return
    help_text = ("List of commands:\n"
                 "/start - Initiate interaction with TheoBot\n"
                 "/help - Get a list of available commands\n"
                 "/register - Register a new user with the bot\n"
                 "/project - Add new project to Jira\n"
                 "/assignrole - Assign roles to users\n"
                 "/createtask - Create a new task within a project\n"
                 "/assigntask - Assign a task to a team member\n"
                 "/status - Check the status of a task\n"
                 "/calendar - View the Theometrics Calendar\n"
                 "/addevent - Add Event to the Theometrics Calendar\n"
                 "/rsvp - RSVP for calendar event\n"
                 "/settings - View or Edit Account Settings\n"
                 "/feedback - Provide feedback about the bot\n"
                 "More features coming soon!")
    update.message.reply_text(help_text)

def register(update, context):
    if not is_user_allowed(update, context):
        return
    keyboard = [
        [InlineKeyboardButton("Show me your Bevis", callback_data='show_bevis')],
        [InlineKeyboardButton("Create New Bevis", callback_data='create_bevis')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose an option:', reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'show_bevis':
        query.edit_message_text(text="Selected option: Show me your Bevis")
    elif query.data == 'create_bevis':
        query.edit_message_text(text="Selected option: Create New Bevis")


def assignrole(update, context):
    if not is_user_allowed(update, context):
        return
    update.message.reply_text('User role assignment is not yet implemented.')

def project(update, context):
    if not is_user_allowed(update, context):
        return
    update.message.reply_text('Creating a new project is not yet implemented.')

def createtask(update, context):
    if not is_user_allowed(update, context):
        return
    update.message.reply_text('Creating a new task is not yet implemented.')

def assigntask(update, context):
    if not is_user_allowed(update, context):
        return
    update.message.reply_text('Assigning a task is not yet implemented.')
    

def status(update, context):
    if not is_user_allowed(update, context):
        return
    update.message.reply_text('Checking task status is not yet implemented.')

def feedback(update, context):
    if not is_user_allowed(update, context):
        return
    update.message.reply_text('Feedback mechanism is not yet implemented.')

def calendar(update, context):
    if not is_user_allowed(update, context):
        return
    update.message.reply_text('Viewing the calendar is not yet implemented.')

def addevent(update, context):
    if not is_user_allowed(update, context):
        return
    update.message.reply_text('Submitting an event is not yet implemented.')

def rsvp(update, context):
    if not is_user_allowed(update, context):
        return
    update.message.reply_text('RSVP to an event is not yet implemented.')


def settings(update, context):
    if not is_user_allowed(update, context):
        return
    update.message.reply_text('Settings are not yet implemented.')

def feedback(update, context):
    if not is_user_allowed(update, context):
        return
    update.message.reply_text('Feedback functionality will be implemented.')
