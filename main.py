from re import X
import telegram
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters, JobQueue
import logging
import datetime
from functions import format_date, start, add, delete, list, check_date, find_bday, format_date, check_bday


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

api_key = "5222251611:AAGd36k-EsuArRem-ahHjUo-vGkYwiHO0l4"

add_1, add_2, delete_1, delete_2 = range(4)


def add_name(update: telegram.Update, context: CallbackContext):
    # Get name
    update.message.reply_text("Name?")

    return add_1

def add_date(update: telegram.Update, context: CallbackContext):
    data = context.user_data
    data["name"] = update.message.text
    # Get date
    update.message.reply_text("Birthdate in the format DDMM")

    return add_2

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

def delete_name(update: telegram.Update, context: CallbackContext):
    # Get name
    update.message.reply_text("Name?")

    return delete_1

def delete_date(update: telegram.Update, context: CallbackContext):
    data = context.user_data
    data["name"] = update.message.text
    
    # Get date
    update.message.reply_text("Birthdate in the format DDMM")

    return delete_2

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

def remind(update: telegram.Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    
    # For testing purposes
    # context.job_queue.run_once(callback=check_bday, when=3, context=chat_id)

    # Run check_bday daily
    context.job_queue.run_daily(callback=check_bday, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=0, minute=0, second=00), context=chat_id)

    context.bot.send_message(chat_id=chat_id, text="Reminder activated. I will remind you of any birthdays each day at 0000H.")


def main():

    # Create dispatcher
    updater = Updater(token=api_key)
    dispatcher = updater.dispatcher


    # Dictionary of non-conversation commands: /start and /list
    commands = {
        "start": CommandHandler('start', start),
        "list": CommandHandler('list', list)
    }

    # Register /start and /list
    for command in commands:
        dispatcher.add_handler(commands[command])
    
    # /add conversation handler
    add_convohandler = ConversationHandler(
        entry_points=[CommandHandler('add', add_name), CommandHandler('delete', delete_name), CommandHandler('remind', remind)],
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
            ]
        },
        fallbacks=[],
    )

    dispatcher.add_handler(add_convohandler)

    # Poll updates from bot
    updater.start_polling()

    # Start webhook
    # updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    # updater.bot.setWebhook('https://yourherokuappname.herokuapp.com/' + TOKEN)

    
if __name__ == '__main__':
    main()