#!/usr/bin/python

import telebot
from telebot import types
import sys
import logging
import datetime
import signal
import os

### CLOSING ###

# Function for close the bot when interrupt command is given

def close_bot(signum, frame):
    logging.warning("KeyboardInterrupt")
    exit()

### LOGGING ###

# Set log file's name as the date and hour of the time of execution

date = datetime.datetime.now()
year = str(date.year)
if date.month < 10:
    month = '0' + str(date.month)
else:
    month = str(date.month)
if date.day < 10:
    day = '0' + str(date.day)
else:
    day = str(date.day)
if date.hour < 10:
    hour = '0' + str(date.hour)
else:
    hour = str(date.hour)
if date.minute < 10:
    minute = '0' + str(date.minute)
else:
    minute = str(date.minute)

if date.second < 10:
    second = '0' + str(date.second)
else:
    second = str(date.second)
datelog = year + month + day + '_' + hour + minute + second

# Set log file's location under the python file's directory

if os.name == 'nt':
    SLASH = '\\'
else:
    SLASH = '/'

dir_log = 'bot_log'
if not os.path.exists('.' + SLASH + dir_log):
    os.makedirs('.' + SLASH + dir_log)

name_log = 'bot_' + datelog + '.log'
log_location = dir_log + SLASH+ name_log

# Set the logging configuration, in INFO by default

#logger = telebot.logger
#logger.basicConfig(filename=name_log, level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

# Logging level = DEBUG
#logging.basicConfig(filename=log_location, level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

# Logging level = INFO
logging.basicConfig(filename=log_location, level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')

# Logging level = WARNING
#logging.basicConfig(filename=log_location, level=logging.WARNING, format=' %(asctime)s - %(levelname)s - %(message)s')

# Logging level = ERROR
#logging.basicConfig(filename=log_location, level=logging.ERROR, format=' %(asctime)s - %(levelname)s - %(message)s')

# Logging level = CRITICAL
#logging.basicConfig(filename=log_location, level=logging.CRITICAL, format=' %(asctime)s - %(levelname)s - %(message)s')

### TELEGRAM BOT ###

# Here goes the Telegram Token:

TOKEN = ""
knownUsers = [ ]

# Function to send the message to users

def sendData(message):
    try:
        bot.sen_message(message)
    except:
        logging.error("Error sending message, usr_id: " + uid)

# Defined commands

commands = {
    'start': 'Activate bot',
    'help': 'Show help menu'
        }

menu = types.ReplyKeyboardMarkup()
menu.add("help")

# Function for manage the users in the list knownUsers

def get_user(uid):
    if not uid in knownUsers:
        knownUsers.append(uid)
        logging.info("New user uid: " + uid)

# Function for listen and log the user's messages

def listener(message):
    for m in message:
        if m.content_type == 'text':
            logging.info("[" + str(m.chat.id) + "] " + str(m.chat.first_name) + ": " + m.text)

# Set the bot configuration for the connection and the listener function

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)

# Start command

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    bot.send_message(cid, 'Activando bot')

# Help command

help_text = 'This bot removes the tokens from any link'
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    bot.send_message(cid, help_text)

# Remove any token from any user's message, detecting where is the question mark and deleting all the rest of the message; this includes any non-link messages

@bot.message_handler(func=lambda message: True)
def echo_message(m):
    link = m.text
    find_q = 0
    if '?' in link:
        for n in range(0, len(link)):
            if link[n] == '?':
                find_q = n
                continue
        bot.reply_to(m, m.text[0:find_q])
    else:
        bot.reply_to(m, m.text)

# Set the keyboard interrupt signal for close the bot

signal.signal(signal.SIGINT, close_bot)

# Loop for the bot connections

while True:
    try:
        bot.polling(none_stop = True)
    except Exception as ex:
        logging.error(str(ex))

