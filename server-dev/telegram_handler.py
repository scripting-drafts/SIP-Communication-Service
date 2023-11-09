from functools import wraps
import logging
import random
from telegram.ext.filters import Filters

from telegram.ext.messagehandler import MessageHandler
from settings import BOT_TOKEN
from telegram import Update
from telegram.ext import (Updater,
                          PicklePersistence,
                          CommandHandler,
                          CallbackQueryHandler,
                          CallbackContext,
                          ConversationHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

from gpt_j_6b import gpt_j_6B
from time import sleep

EXPECT_NAME, EXPECT_BUTTON_CLICK = range(2)
NUMEXPR_MAX_THREADS = 12
LIST_OF_ADMINS = [19419361]
gpt = gpt_j_6B()

def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped

@restricted
def start(update: Update, context: CallbackContext):
    ''' Replies to start command '''
    update.message.reply_text('just a sec')
    while True:
        try:
            reply = gpt.get_payload()
            update.message.reply_text(reply)
            sleep(random.uniform(60.*60, 120.*60))
        except KeyboardInterrupt:
            break

    return ConversationHandler.END

# For images - 'Generating reply'
@restricted
def button_click_handler(update: Update, context: CallbackContext):
    ''' This gets executed on button click '''
    query = update.callback_query
    # shows a small notification inside chat
    query.answer(f'button click {query.data} recieved')

    if query.data == 'name':
        query.edit_message_text(f'You clicked on "name"')
        # asks for name, and prompts user to reply to it
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send your name', reply_markup=ForceReply())
        # learn more about forced reply
        # https://python-telegram-bot.readthedocs.io/en/stable/telegram.forcereply.html
        return EXPECT_NAME

@restricted
def simple_reply(update: Update, context: CallbackContext):
    user_input = update.message.text
    answer = 'henlo'
    update.message.reply_text(answer)

    return ConversationHandler.END

if __name__ == "__main__":
    pp = PicklePersistence(filename='mybot')
    updater = Updater(token=BOT_TOKEN, persistence=pp)

    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    _handlers = {}
    _handlers['start_handler'] = CommandHandler('start', start)

    for name, _handler in _handlers.items():
        print(f'Adding handler {name}')
        dispatcher.add_handler(_handler)

    updater.start_polling()

    updater.idle()