from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import logging
import os

from prep_excel import excel_to_geo_png

import config

logging.basicConfig(filename='bot.log', level=logging.INFO)


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Получите заказ с помощью команды /order")


def handle_reply_files(update: Update, context: CallbackContext):
    message = update.message.reply_to_message
    if message and message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name

        file = context.bot.get_file(file_id)
        file.download(file_name)

        cardinal_direction = excel_to_geo_png(file_name, config.PNG_NAME)

        context.bot.send_photo(chat_id=update.message.chat_id,
                               photo=open(config.PNG_NAME, 'rb'),
                               caption=cardinal_direction)

        os.remove(config.PNG_NAME)


def main() -> None:
    updater = Updater(config.TOKEN_TG,
                      use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.reply, handle_reply_files))

    logging.info('Bot started')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
