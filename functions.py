from html import entities
import telegram
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler
import sqlite3


def start(update: telegram.Update, context: CallbackContext):
    # Intro text
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm a birthday reminder bot. I help you set reminders for birthdays!")

    # List of commands
    context.bot.send_message(chat_id=update.effective_chat.id, text="<b>Commands</b>: \n/add - Add a new birthday \n/delete - Delete an existing birthday \n/remind - Set reminder \n/list - List all existing birthdays", parse_mode=telegram.constants.PARSEMODE_HTML)

       
def add(update: telegram.Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Name?")


def delete(update: telegram.Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Fuck")

def remind(update: telegram.Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Fuck")

def list(update: telegram.Update, context: CallbackContext):
    # Query db for all birthdays
    # Connect to db
    con = sqlite3.connect("bday.db")
    cursor = con.cursor()

    list = cursor.execute("SELECT Name, Birthdate FROM people")
    
    
    while(list[i]):
        context.bot.send_message(chat_id=update.effective_chat.id, text="", entities=)