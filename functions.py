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
    # Connect to database
    con = sqlite3.connect("bday.db")
    cursor = con.cursor()
    
    try:
        # Add to db
        cursor.execute("INSERT INTO people (Name, Birthdate) VALUES (?, ?)", (name, date))
        con.commit()
        return True
    
    except:
        return False

def delete(name: str, date: str):
    # Connect to db
    con = sqlite3.connect("bday.db")
    cursor = con.cursor()
    
    try:
        # Delete from db
        cursor.execute("DELETE FROM people WHERE Name = ? AND Birthdate = ?", (name, date))
        con.commit()
        return True

    except:
        return False


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
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"{format_date(date)}: {row[0]}'s birthday")


# Function to check if date is valid, returns true if valid
def check_date(date: str):
    # Check length of date str
    if len(date) != 4:
        return False

    dd = int(date[0] + date[1])
    mm = int(date[2] + date[3])

    # Ensure date and month in correct range
    if (0 < dd < 32) and (0 < mm < 13): 
        # Check for months where last day is 30
        if mm in [2, 4, 6, 9, 11] and dd == 31:
            return False

        return True

    return False

    
def find_bday(name: str, date: str):
    # Connect to db
    con = sqlite3.connect("bday.db")
    cursor = con.cursor()
    person = cursor.execute("SELECT * FROM people WHERE Name = ? AND Birthdate = ?", (name, date)).fetchall()
    if person:
        return True
    else:
        # Person is an empty list, meaning the data does not exist in db 
        return False


# Formats date from DDMM to DD/MM
def format_date(date: str):
    return date[0] + date[1] + '/' + date[2] + date[3]