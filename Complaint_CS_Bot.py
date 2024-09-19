
import logging

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

import ai.chat_ai;
import messenger;

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# States of conversation handler
(MAIN_LEVEL, SECOND_LEVEL) = range(2)

# MAIN_LEVEL
GENERAL_COMPLAINT = "General complaint"
ORDER_NOT_RECEIVED = "Order not received"
GOODS_DAMAGED = "Goods are not as described or damaged"
mainKeyboard = [[GENERAL_COMPLAINT], [ORDER_NOT_RECEIVED], [GOODS_DAMAGED]]

# SECOND_LEVEL
REDELIVERY = "Redelivery"
REFUND = "Refund"
MAIN_KEYBOARD = "Back to main menu"
secondKeyboard = [[REDELIVERY], [REFUND], [MAIN_KEYBOARD]]


# Start function. It gets called only once in the beginning of each session
def start(update, context):
    user = update.message.from_user
    logger.info('Bot session started.')
    greeting = 'Hey {}, I am Customer Complaint Chatbot. With my help you can maximize your chances for a successful complaint!\n\n'.format(user.first_name)
    greeting += 'Please, select the type of your complaint or describe your problem!'
    reply_markup = ReplyKeyboardMarkup(mainKeyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text(greeting, reply_markup=reply_markup)
    return MAIN_LEVEL


# Function processes the choice made on the main keyboard
def main_level(update, context):
    user = update.message.from_user
    selected = update.message.text
    logger.info("User %s selected option %s", user.first_name, selected)

    if selected == GENERAL_COMPLAINT:
        message = messenger.generalComplaint();
        reply_markup = ReplyKeyboardMarkup(mainKeyboard, resize_keyboard=True, one_time_keyboard=False)
        update.message.reply_text(message, parse_mode='HTML', reply_markup=reply_markup)
        return MAIN_LEVEL

    elif selected == ORDER_NOT_RECEIVED:
        message = messenger.orderNotReceived();
        reply_markup = ReplyKeyboardMarkup(mainKeyboard, resize_keyboard=True, one_time_keyboard=False)
        update.message.reply_text(message, parse_mode='HTML', reply_markup=reply_markup)
        return MAIN_LEVEL

    elif selected == GOODS_DAMAGED:
        reply_markup = ReplyKeyboardMarkup(secondKeyboard, resize_keyboard=True, one_time_keyboard=False)
        update.message.reply_text('Please, select one of the options.', reply_markup=reply_markup)
        return SECOND_LEVEL;

    else:
        ai_response(update)
        return MAIN_LEVEL;

# Function processes the choice made on the social media keyboard
def second_level(update, context):
    user = update.message.from_user
    selected = update.message.text
    logger.info("User %s selected option %s", user.first_name, selected)

    if selected == REDELIVERY:
        message = messenger.reDelivery(user.first_name)
        reply_markup = ReplyKeyboardMarkup(secondKeyboard, resize_keyboard=True, one_time_keyboard=False)
        update.message.reply_text(message, parse_mode='HTML', reply_markup=reply_markup)
        return SECOND_LEVEL

    elif selected == REFUND:
        message = messenger.reFund(user.first_name)
        reply_markup = ReplyKeyboardMarkup(secondKeyboard, resize_keyboard=True, one_time_keyboard=False)
        update.message.reply_text(message, parse_mode='HTML', reply_markup=reply_markup)
        return SECOND_LEVEL

    elif selected == MAIN_KEYBOARD:
        reply_markup = ReplyKeyboardMarkup(mainKeyboard, resize_keyboard=True, one_time_keyboard=False)
        update.message.reply_text('Choose an option with the buttons below.', reply_markup=reply_markup)
        return MAIN_LEVEL;

    else:
        ai_response(update)
        return SECOND_LEVEL;

def ai_response(update):
    user = update.message.from_user
    res = ai.chat_ai.chatbot_response(update.message.text)

    if res == GENERAL_COMPLAINT:
        message = messenger.generalComplaint()
        update.message.reply_text(message, parse_mode='HTML')

    elif res == ORDER_NOT_RECEIVED:
        message = messenger.orderNotReceived()
        update.message.reply_text(message, parse_mode='HTML')

    elif res == REDELIVERY:
        message = messenger.reDelivery(user.first_name)
        update.message.reply_text(message, parse_mode='HTML')

    elif res == REFUND:
        message = messenger.reFund(user.first_name)
        update.message.reply_text(message, parse_mode='HTML')

    else:
        update.message.reply_text(res)

def help(update, context):
    # message on /help
    update.message.reply_text('Help!')

def error(update, context):
    update.message.reply_text("We are sorry, it seems there is an error!")
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater('1854111230:AAFQLXMlJBzIrbYlpKGZ1I_uE2W90MFF8vQ', use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points = [MessageHandler(Filters.text, start), CommandHandler('start', start)],

        states={
            MAIN_LEVEL: [MessageHandler(Filters.text & ~Filters.command, main_level)],
            SECOND_LEVEL: [MessageHandler(Filters.text & ~Filters.command, second_level)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
