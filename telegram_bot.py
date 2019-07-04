token = '873581678:AAF0JY0SosaAOtJ1hxiYo1po38G1VRdfdGs'

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from read_data import read_log_file

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

help_str = """for past weather, type: /how
for more details, type: /details
"""

details_str = """Using rain cloud data (updated every 5 min) from NEA, this bot displays the times when those rain clouds intersect with a pre-defined boundaries of dairy farm climbing locations. Rain intensities range from 0 (light rain) - 100 (heavy rain)
"""

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(help_str)

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(help_str)
    
def how(update, context):
    update.message.reply_text(read_log_file())

def details(update, context):
    update.message.reply_text(details_str)
    
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("how", how))    
    dp.add_handler(CommandHandler("details", details))
    
    # on noncommand i.e message
#    dp.add_handler(MessageHandler(Filters.text, reply))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
