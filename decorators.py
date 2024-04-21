from config import admins

def admin_only(func):
    def wrapper(update, context):
        if update.message.chat_id in admins:
            return func(update, context)
        return -1
    return wrapper
