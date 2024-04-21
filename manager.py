from telegram.ext import CommandHandler, MessageHandler, Updater, ConversationHandler, Filters, CallbackQueryHandler

from handlers import start, choice, query_handler, get_user_name, create_user
from config import TOKEN
from openvpn import init_db

import logging


logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
            )

logger = logging.getLogger(__name__)

def main():
    updater = Updater(TOKEN, request_kwargs={'proxy_url': 'socks5h://127.0.0.1:1234'})
    dp = updater.dispatcher

    dp.add_handler(ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states = {
            1: [MessageHandler(Filters.regex('^(Manage current clients|Add a new Client)$'), choice), MessageHandler(Filters.all, start)],
            2: [MessageHandler(Filters.text, get_user_name)],
            3: [MessageHandler(Filters.regex('^(\/skip|[0-9]+)$'), create_user)]
        },
        fallbacks = []
    ))

    dp.add_handler(CallbackQueryHandler(query_handler))

    init_db()

    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()
