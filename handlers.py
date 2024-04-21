from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from decorators import admin_only
from helpers import (users_keyboard, manage_user_keyboard,
        yes_no_keyboard, user_stats_keyboard, user_stats_message)

from openvpn import revoke, get_users, add_user, get_config

import string, re


@admin_only
def start(update, context):
    keyboard = [['Manage current clients'], ['Add a new Client']]
    update.message.reply_text("Welcome, How can I help you?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))

    return 1

@admin_only
def choice(update, context):
    if 'Manage' in update.message.text:
        update.message.reply_text("Here you can see the list of users:", reply_markup=users_keyboard())
        return 1 
    update.message.reply_text("Send me the name of the new client")
    return 2

def get_user_name(update, context):
    if update.message.text=='/start':
        return start(update, context)
    name = update.message.text
    if (set(name)-set(string.printable[:61])):
        update.message.reply_text('This name contains illegal characters.\nSend me another one')
        return 2

    if name in get_users():
        update.message.reply_text('This name already exists\nTry another one')
        return 2

    context.user_data['user_name'] = name
    update.message.reply_text("How many days of membership do you want for this user?\nEnter /skip if you don't want it to expire.")
    return 3 # Get days or none

def create_user(update, context):
    if update.message.text.startswith('/skip'):
        days = None
    else:
        days = int(update.message.text)
    name = context.user_data['user_name']
    try:
        add_user(name, days)
    except Exception as e:
        update.message.reply_text("An error has occured, \start to start over")
        return -1
    update.message.reply_text(f'User "{name}" has been created.\nSend another name if you want to add another one, or hit /start to start over')
    return 2

def query_handler(update, context):
    query = update.callback_query

    if query.data.startswith('page'):
        query.message.edit_text(query.message.text, reply_markup=users_keyboard(int(query.data[5:])))
        query.answer('Switched to page: '+query.data[5:])

    elif query.data.startswith('user'):
        user = query.data[5:query.data.rfind('?')]
        query.message.edit_text('Now what do you want to do with '+user, reply_markup=manage_user_keyboard(query.data[5:]))
        query.answer()

    elif query.data.startswith('revoke'):
        user = query.data[7:-2]
        query.message.edit_text(f'You are attempting to remove user: "{user}"\nAre you sure about that?', reply_markup=yes_no_keyboard(query.data[7:]))
        query.answer()

    elif query.data.startswith('sudo_revoke'):
        user, page = query.data[12:].split('?')
        success = revoke(user)

        if success:
            query.answer('Access of user %s has been revoked' % query.data[12:])

        else:
            query.answer("User doesn't exist!")
        query.message.edit_text('Here you can see the list of users:', reply_markup=users_keyboard(int(page)))

    elif query.data.startswith('config'):
        name, page = query.data[7:].split('?')

        config_file = get_config(name)
        if config_file:
            with open('configs/'+config_file, 'rb') as f:
                context.bot.send_document(query.message.chat_id, f)
            query.answer()
        else:
            query.message.reply_text("Something went wrong.")

    elif query.data.startswith('stats'):
        data = query.data[6:]
        query.message.edit_text(user_stats_message(data), reply_markup=user_stats_keyboard(data))
        query.answer()
