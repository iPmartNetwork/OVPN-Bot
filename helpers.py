from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from openvpn import get_users, exec_db

def users_keyboard(page=1):
    users = get_users()
    if not users:
        return None

    keyboard = []
    if page==1:
        page_users = users[:20]
    else:
        page_users = users[page*20-20:page*20]

    if not page_users:
        return users_keyboard(page-1)

    for i in range(0, 20, 2):
        keyboard.append([InlineKeyboardButton(btn, callback_data='user_'+btn+'?'+str(page)) for btn in page_users[i:i+2]])

    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton('← Back', callback_data='page_'+str(page-1)))

    if users[page*20:]:
        nav_buttons.append(InlineKeyboardButton('Next →', callback_data='page_'+str(page+1)))

    keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(keyboard)

def manage_user_keyboard(data):
    user, page = data.split('?')

    keyboard = [[
        InlineKeyboardButton('Revoke access', callback_data=f'revoke_{user}?{page}'),
        InlineKeyboardButton('See stats', callback_data=f'stats_{user}?{page}')
        ],
        [
            InlineKeyboardButton('Get configuration file', callback_data=f'config_{user}?{page}')
        ],
        [
            InlineKeyboardButton('Return to users list', callback_data='page_'+page)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def yes_no_keyboard(data):

    print('data', data)
    user, page = data.split('?')
    keyboard = [
        [
            InlineKeyboardButton('Yes', callback_data=f'sudo_revoke_{user}?{page}'),
            InlineKeyboardButton('No', callback_data=f'user_{user}?{page}')
        ]
    ]

    return InlineKeyboardMarkup(keyboard)

def user_stats_keyboard(data):
    user, page = data.split('?')
    keyboard = [
        [
            InlineKeyboardButton('Users list', callback_data='page_'+page),
            InlineKeyboardButton('Back to user', callback_data=f'user_{user}?{page}')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def user_stats_message(data):
    user = data.split('?')[0]
    date, days = exec_db('SELECT register_date, days FROM users WHERE name = ?', (user,), fetch=True)[0]
    message = f'Name: {user}\nRegistration date: {date}'
    if days:
        message += f'\nDays left: {days}'

    return message
