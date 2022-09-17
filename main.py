import telegram
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters
import logging
from functions import start, add, delete, remind, list

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

api_key = "5222251611:AAGd36k-EsuArRem-ahHjUo-vGkYwiHO0l4"


def add_name(update: telegram.Update, context: CallbackContext):
    # Get name
    update.message.reply_text("Name?")

    return 1

def add_date(update: telegram.Update, context: CallbackContext):
    global name 
    name = update.message.text
    # Get date
    update.message.reply_text("Birthdate in the format DDMMYY")

    return 2

def add_last(update: telegram.Update, context: CallbackContext):
    date = update.message.text

    if add(name, date):
        update.message.reply_text("Birthday successfully added!")
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"{name} {date}")


    return ConversationHandler.END

def main():

    # Create dispatcher
    updater = Updater(token=api_key)
    dispatcher = updater.dispatcher


    # Dictionary of commands excluding /list
    commands = {
        "start": CommandHandler('start', start),
        "delete": CommandHandler('delete', delete),
        "remind": CommandHandler('remind', remind)
    }

    # Register /list command
    list_handler = CommandHandler('list', list)
    dispatcher.add_handler(list_handler) 

    for command in commands:
        dispatcher.add_handler(commands[command])
    
    # /add conversation handler
    add_convohandler = ConversationHandler(
        entry_points=[CommandHandler("add", add_name)],
        states={
            1: [
                MessageHandler(Filters.text, add_date)
            ],
            2: [
                MessageHandler(Filters.text, add_last)
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