# Telegram Birthday Bot
A telegram bot that allows users to keep track of birthdays. The bot is written in python using the python-telegram-bot package and keeps track of birthdays using a SQL database. 
## Video Demo: <URL>
### **List of bot commands:**
- /start
- /add
- /delete
- /remind
- /list
### **/start**: 
Introduces the bot and lists the other available commands.

<br>

### **/add**: 
Adds a birthday into the list by giving name and birthdate in the format DDMM as prompted by the bot in a simple conversation. Rejects user input if invalid date is given. 

<br>

### **/delete**: 
Delete a birthday from the list by giving name and birthdate in the format DDMM as prompted by the bot in a simple conversation. If birthday given is not in the birthday list, the bot will tell the user so. 

<br>

### **/remind**: 
Set reminder for bot so at every day at specificed HHMM timing the bot checks the list of birthdays and reminds the user of any birthdays that fall on the current date. Bot rejects time input if invalid time is given.

<br>

### **/list**: 
List all the birthdays in the list in alphabetical order. If list contains no birthdays, bot will say so.

<br>

## **Project Description**
This bot is hosted on the cloud hosting service Heroku. Unfortunately, as this bot is hosted under its free service, the bot sleeps after 30 minutes of inactivity, thus the /remind feature does not work unless the service is upgraded to Heroku's paid service such that the bot runs 24/7 such that everyday at the specified timing the bot checks the birthday list for any birthdays to remind the user.

<br>

The telebot_project folder contains the 2 python files, main.py and functions.py. The main.py file contains the main function and some functions to handle the bot conversations involved in /add, /delete and /remind. The functions.py file contains functions that connect to the SQL database bday.db and also format dates and times in the relevant format. 

<br>

Finally, the Procfile is for Heroku to know what to execute when running the code on its cloud platform. The requirements.txt file lists the various required packages for the telegram bot to work, namely version 13 of the python-telegram-bot python package.

<br>

## Limitations
Apart from the impractical issue of the remind function which can be rectified by upgrading to Heroku's paid service, another limitation of the bot is that its use is limited to only one user. As a single database (bday.db) is used, all the birthdays are stored in the same database such that in the event of multiple bot users, each user is able to access other users' birthdays which is undesirable. A possible solution to this is to create a new unique table in bday.db everytime a new user talks to the bot. Each table then is then uniquely linked to each user so that every user can only access their own table containing their own birthdays. 