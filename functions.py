from ast import Pass
from html import entities
import telegram
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters
import sqlite3


def start(update: telegram.Update, context: CallbackContext):
    # Intro text
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm a birthday reminder bot. I help you set reminders for birthdays!")

    # List of commands
    context.bot.send_message(chat_id=update.effective_chat.id, text="<b>Commands</b>: \n" +
    "/add - Add a new birthday \n" +
    "/delete - Delete an existing birthday \n" +
    "/remind - Set reminder \n" +
    "/list - List all existing birthdays", parse_mode=telegram.constants.PARSEMODE_HTML)



def add(name, date):


    # if update.effective_message:
    #     name = update.message.text
    #     # Get date
    #     context.bot.send_message(chat_id=update.effective_chat.id, text="Birthdate in the format DDMMYY")
    #     date = update.message.text
 
    #     # Add to database
    con = sqlite3.connect("bday.db")
    cursor = con.cursor()
    cursor.execute("INSERT INTO people (Name, Birthdate) VALUES (?, ?)", (name, date))

def add_date(update: telegram.Update, context: CallbackContext):
    name = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text="Date?")
    MessageHandler(Filters.text, add_action(update, context, name))

def add_action(update: telegram.Update, context: CallbackContext, name: str):
    date = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{name} {date}")

def delete(update: telegram.Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Fuck")

def remind(update: telegram.Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Fuck")

def list(update: telegram.Update, context: CallbackContext):
    # Query db for all birthdays
    con = sqlite3.connect("bday.db")
    cursor = con.cursor()
    list = cursor.execute("SELECT Name, Birthdate FROM people")
    
    # Send messages, each being a birthday entry
    for row in list:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"{row[1]}: {row[0]}'s birthday")
