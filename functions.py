import telegram
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, ConversationHandler, Filters, Job
import sqlite3
import datetime

db = "bday.db"


# Start message to introduce bot
def start(update: telegram.Update, context: CallbackContext):
    # Intro text
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm a birthday reminder bot. I help you set reminders for birthdays!")

    # List of commands
    context.bot.send_message(chat_id=update.effective_chat.id, text="<b>Commands</b>: \n" +
    "/add - Add a new birthday \n" +
    "/delete - Delete an existing birthday \n" +
    "/remind - Start reminder function of bot \n" +
    "/list - List all existing birthdays", parse_mode=telegram.constants.PARSEMODE_HTML)


# Add bday to bday.db
def add(name, date):    
    # Connect to database
    con = sqlite3.connect(db)
    cursor = con.cursor()
    
    try:
        # Add to db
        cursor.execute("INSERT INTO people (Name, Birthdate) VALUES (?, ?)", (name, date))
        con.commit()
        return True
    
    except:
        return False

# Delete bday from bday.db
def delete(name: str, date: str):
    # Connect to db
    con = sqlite3.connect(db)
    cursor = con.cursor()
    
    try:
        # Delete from db
        cursor.execute("DELETE FROM people WHERE Name = ? AND Birthdate = ?", (name, date))
        con.commit()
        return True

    except:
        return False


# Check if current date is someone's bday, if so send reminder
def check_bday(context: CallbackContext):
    # Get current date
    today = datetime.date.today()
    ddmm = today.strftime('%d%m')

    # Connect to database
    con = sqlite3.connect(db)
    cursor = con.cursor()
    name_list = cursor.execute("SELECT Name FROM people WHERE Birthdate = ? ORDER BY Name", (ddmm,)).fetchall()

    # Remind birthday if any
    if name_list:
        for row in name_list:
            name = row[0]
            context.bot.send_message(chat_id=context.job.context, text=f"Today is {name}'s birthday!")
    

# Send messages listing all bdays in bday.db
def list_bday(update: telegram.Update, context: CallbackContext):
    # Query db for all birthdays
    con = sqlite3.connect(db)
    cursor = con.cursor()
    list = cursor.execute("SELECT Name, Birthdate FROM people ORDER BY Name")
    
    # Send messages, each being a birthday entry in alphabetical order
    for row in list:
        date = row[1]
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"{row[0]}'s birthday: {format_date(date)}")


# Check if date is valid, returns true if valid
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

    
# Returns True if person and bday exists in db
def find_bday(name: str, date: str):
    # Connect to db
    con = sqlite3.connect(db)
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