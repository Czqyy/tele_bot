import telegram
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters
import logging
from functions import start, add, delete, remind, list, check_date, find_bday

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
            update.message.reply_text(f"{name}'s birthday on {date} successfully added!")
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
            update.message.reply_text(f"{name}'s birthday on {date} deleted.")
            data.clear()
            return ConversationHandler.END

        else:
            update.message.reply_text("Deletion unsuccessful! Please try again with /delete")


def main():

    # Create dispatcher
    updater = Updater(token=api_key)
    dispatcher = updater.dispatcher


    # Dictionary of non-conversation commands: /start and /list
    commands = {
        "start": CommandHandler('start', start),
        "list": CommandHandler('list', list)
    }

    # list_handler = CommandHandler('list', list)
    # dispatcher.add_handler(list_handler) 

    # Register /start and /list
    for command in commands:
        dispatcher.add_handler(commands[command])
    
    # List of conversation handlers: /add, /delete, /remind
    convo_handler_list = []
    convo_handler_list.append(CommandHandler("add", add_name))
    convo_handler_list.append(CommandHandler('delete', delete_name))
    convo_handler_list.append(CommandHandler('remind', remind))


    # /add conversation handler
    add_convohandler = ConversationHandler(
        entry_points=[convo_handler_list],
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
        # NOT FINISHED!
        fallbacks=[CommandHandler("delete", delete)],
    )

    dispatcher.add_handler(add_convohandler)

    # Poll updates from bot
    updater.start_polling()

if __name__ == '__main__':
    main()