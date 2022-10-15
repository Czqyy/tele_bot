import os
import telegram
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters
import logging
import datetime
from functions import format_date, start, add, delete, list_bday, check_date, find_bday, format_date, check_bday


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

api_key = "5222251611:AAGd36k-EsuArRem-ahHjUo-vGkYwiHO0l4"

add_1, add_2, delete_1, delete_2, remind = range(5)


# Starting convo for /add, asking for Name
def add_name(update: telegram.Update, context: CallbackContext):
    # Get name
    update.message.reply_text("Name?")

    return add_1


# /add convo, asking for date
def add_date(update: telegram.Update, context: CallbackContext):
    data = context.user_data
    data["name"] = update.message.text
    # Get date
    update.message.reply_text("Birthdate in the format DDMM")

    return add_2

# Ending convo for /add, adding info to bday.db
def add_last(update: telegram.Update, context: CallbackContext):
    data = context.user_data
    data["date"] = update.message.text

    # Check if date is valid
    if not check_date(data["date"]):
        update.message.reply_text("Date given is invalid! Please try again with /add")
        data.clear()
        return ConversationHandler.END
    
    else:
        if add(data["name"], data["date"]):
            name = data["name"]
            date = data["date"]

            # Reply update
            update.message.reply_text(f"{name}'s birthday on {format_date(date)} successfully added!")
            data.clear
            return ConversationHandler.END

        else:
            update.message.reply_text("Add birthday unsuccessful! Please try again with /add")
            data.clear()
            return ConversationHandler.END


# Start convo for /delete, asking for Name
def delete_name(update: telegram.Update, context: CallbackContext):
    # Get name
    update.message.reply_text("Name?")

    return delete_1


# /delete convo, asking for date
def delete_date(update: telegram.Update, context: CallbackContext):
    data = context.user_data
    data["name"] = update.message.text
    
    # Get date
    update.message.reply_text("Birthdate in the format DDMM")

    return delete_2


# Ending convo for /delete, deleting bday from bday.db
def delete_last(update: telegram.Update, context: CallbackContext):
    data = context.user_data
    data["date"] = update.message.text

    if not find_bday(data["name"], data["date"]):
        update.message.reply_text("Person cannot be found. Please try again with /delete")
        data.clear()
        return ConversationHandler.END

    else:
        if delete(data["name"], data["date"]):
            name = data["name"]
            date = data["date"]

            # Reply update
            update.message.reply_text(f"{name}'s birthday on {format_date(date)} deleted.")
            data.clear()
            return ConversationHandler.END

        else:
            update.message.reply_text("Deletion unsuccessful! Please try again with /delete")
            data.clear()
            return ConversationHandler.END


# Start convo of /remind, asking for time
def remind_time(update: telegram.Update, context: CallbackContext):
    # Get time
    update.message.reply_text("Time of reminder in HHMM format?")

    return remind

# Set reminder
def set_reminder(update: telegram.Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    
    # Check validity of message
    time = update.message.text

    # Check if message is numeric
    if not time.isnumeric():
        update.message.reply_text("Please enter numbers only, try again.")

        return remind

    # Format time given
    hh = int(time[0] + time[1])
    mm = int(time[2] + time[3])

    # Check validity of time
    if hh not in list(range(0, 24)) or mm not in list(range(0, 60)):
        update.message.reply_text("Invalid time given, try again.")

        return remind

    # Convert to local time (UTC+8)
    hh -= 8
    if hh < 0:
        hh += 24

    # Run check_bday daily
    context.job_queue.run_daily(callback=check_bday, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=hh, minute=mm, second=00), context=chat_id)

    context.bot.send_message(chat_id=chat_id, text=f"Reminder activated. I will remind you of any birthdays each day at {time}H.")

    return ConversationHandler.END



def main():

    # Create dispatcher
    updater = Updater(token=api_key)
    dispatcher = updater.dispatcher


    # Dictionary of non-conversation commands: /start and /list
    commands = {
        "start": CommandHandler('start', start),
        "list": CommandHandler('list', list_bday)
    }

    # Register /start and /list
    for command in commands:
        dispatcher.add_handler(commands[command])
    
    # /add conversation handler
    add_convohandler = ConversationHandler(
        entry_points=[CommandHandler('add', add_name), CommandHandler('delete', delete_name), CommandHandler('remind', remind_time)],
        states={
            add_1: [
                MessageHandler(Filters.text, add_date)
            ],
            add_2: [
                MessageHandler(Filters.text, add_last)
            ],
            delete_1: [
                MessageHandler(Filters.text, delete_date)
            ],
            delete_2: [
                MessageHandler(Filters.text, delete_last)
            ],
            remind: [
                MessageHandler(Filters.text, set_reminder)
            ]
        },
        fallbacks=[],
        allow_reentry=True
    )

    dispatcher.add_handler(add_convohandler)

    # Poll updates from bot
    updater.start_polling()

    # Start webhook
    # updater.start_webhook(listen="0.0.0.0", port=int(os.environ.get('PORT', 5000)), url_path=api_key)
    # updater.bot.set_webhook('https://evening-refuge-42889.herokuapp.com/' + api_key)

    
if __name__ == '__main__':
    main()