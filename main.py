import telegram
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler
import logging
from functions import start, add, delete, remind, list

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

api_key = "5222251611:AAGd36k-EsuArRem-ahHjUo-vGkYwiHO0l4"
user_id = "1802361134"


def main():
    # Create bot object
    bot = telegram.Bot(token=api_key)

    # Create dispatcher
    updater = Updater(token=api_key)
    dispatcher = updater.dispatcher


    # Dictionary of commands excluding /list
    commands = {
        "start": CommandHandler('start', start),
        "add": CommandHandler('add', add),
        "delete": CommandHandler('delete', delete),
        "remind": CommandHandler('remind', remind)
    }

    # Register /list command
    list_handler = CommandHandler('list', list)
    dispatcher.add_handler(list_handler) 

    for command in commands:
        dispatcher.add_handler(commands[command])
    

    # Add conversation handler
    convo_handler = ConversationHandler(
        entry_points=[list(commands.values())],
        states={
            Name: 
        }
    )

    # Poll updates from bot
    updater.start_polling()

if __name__ == '__main__':
    main()