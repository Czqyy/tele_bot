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
    try:
        # Add to database
        con = sqlite3.connect("bday.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO people (Name, Birthdate) VALUES (?, ?)", (name, date))
        con.commit()
        return True
    except:
        return False

def delete(name: str, date: str):
    



    
def remind(update: telegram.Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Fuck")

def list(update: telegram.Update, context: CallbackContext):
    # Query db for all birthdays
    con = sqlite3.connect("bday.db")
    cursor = con.cursor()
    list = cursor.execute("SELECT Name, Birthdate FROM people")
    
    # Send messages, each being a birthday entry
    for row in list:
        date = row[1]
        formatted_date = date[0] + date[1] + "/" + date[2] + date[3]
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"{formatted_date}: {row[0]}'s birthday")


# Function to check if date is valid, returns true if valid
def check_date(date: str):
    # Check length of date str
    if len(date) != 4:
        return False

    dd = int(date[0] + date[1])
    mm = int(date[2] + date[3])

    if dd < 1 or dd > 31: 
        return False

    elif mm < 1 or mm > 12:
        return False

    # Check for months where last day is 30
    elif mm in [2, 4, 6, 9, 11]:
        if dd > 30: 
            return False

    else:
        return True

    
def find_bday(name: str, date: str):
