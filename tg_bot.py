#!/usr/bin/python
# -*- coding: utf-8 -*-

from telegram import *
from telegram.ext import *
import coloredlogs, logging
from datetime import timedelta, datetime, time
from pytz import timezone, UTC

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


class TelegramBot:
    def __init__(self):
        token = '1111327991:AAEfAijEz68wdHdVwFL53LYeuWVf9vuypTY'  # test bot
        # token = '5562371099:AAE-s2UU7w6QbQCV9lCubBLVWHjpb4QMAC0'

        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher

        self.tmp_data = {}

        text_filter = ~Filters.command(False)

        self.dispatcher.add_handler(CommandHandler('start', self.weekly_job, pass_job_queue=True))
        self.dispatcher.add_handler(CommandHandler('chat_id', self.chat_id))
        self.dispatcher.add_handler(
            ConversationHandler(
                entry_points=[MessageHandler(Filters.regex('Давай по классике, вдарим красного'), self.second_question,
                                             pass_job_queue=True),
                              MessageHandler(Filters.regex('Давай лёгонького беленького'), self.second_question,
                                             pass_job_queue=True),
                              MessageHandler(Filters.regex('Ой, хочется пузырёчков'), self.second_question,
                                             pass_job_queue=True),
                              MessageHandler(Filters.regex('К чёрту вино'), self.second_question, pass_job_queue=True)],
                states={1: [MessageHandler(Filters.regex('Красное'), self.third_question),
                            MessageHandler(Filters.regex('Белое'), self.third_question),
                            MessageHandler(Filters.regex('Розовое'), self.third_question)],
                        2: [MessageHandler(Filters.regex('Сухое'), self.send_to_courier),
                            MessageHandler(Filters.regex('Полусухое'), self.send_to_courier),
                            MessageHandler(Filters.regex('Полусладкое'), self.send_to_courier),
                            MessageHandler(Filters.regex('Сладкое'), self.send_to_courier)]},
                fallbacks=[CommandHandler("cancel", self.start),
                           MessageHandler(Filters.regex("Назад"), self.start)]))
        self.dispatcher.add_handler(MessageHandler(text_filter, self.send_non_msg))

        coloredlogs.install()
        # dispatcher.add_error_handler(lambda update, context, error: print(f'ERROR OCCURRED: {error}'))

    def run(self):
        self.updater.start_polling()

    def weekly_job(self, update, context: CallbackContext):
        self.send_message(update, "Ира, с днём рождения! А что умеет этот бот, ты узнаешь завтра")
        # context.job_queue.run_repeating(self.start, interval=timedelta(weeks=1),
        #                                 first=datetime(year=2022, month=11, day=16,
        #                                                hour=1, minute=28) - datetime.now(),
        #                                 context=context)
        context.job_queue.run_repeating(self.start, interval=timedelta(weeks=1),
                                        first=timedelta(seconds=1),
                                        context=update.message.chat_id)
        context.job_queue.start()
        return ConversationHandler.END

    def start(self, context):
        ### добавить проверку на пользователя
        keyboard = [
            ['Давай по классике, вдарим красного'],
            ['Давай лёгонького беленького'],
            ['Ой, хочется пузырёчков'],
            ['К чёрту вино']
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard)
        self.updater.bot.send_message(chat_id=context.job.context, text="Эта пятница не обойдётся без вина. Какое?",
                                      reply_markup=reply_markup)
        return 1

    def second_question(self, update, context):
        print('хуй')
        return 1

    def third_question(self, update, context):

        return 2

    def send_to_courier(self, update, context):
        self.wine_cual = update.message.text
        context.bot.send_message(chat_id=460209939, text=f"Настроение: {self.mood}\n"
                                                         f"Хочет {self.wine_color} {self.wine_cual}")
        context.bot.send_message(chat_id=363972614, text=f"Настроение: {self.mood}\n"
                                                         f"Хочет {self.wine_color} {self.wine_cual}")
        self.send_message(update, "Курьеру направлена информация, жди его сегодня после 18 часов\n\n"
                                  'Чтобы выбрать вино на следующую неделю просто напиши "Хочу вина!"')
        return ConversationHandler.END

    def chat_id(self, update, context):
        print(update.message.chat_id)
        return ConversationHandler.END

    def send_non_msg(self, update, context):
        msg = update.message.text
        if update.message.chat_id == 460209939 or update.message.chat_id == 316284874:
            context.bot.send_message(chat_id=000000000000000000000000000000, text=msg)
        context.bot.send_message(chat_id=460209939, text=msg)
        return ConversationHandler.END

    def send_message(self, update, msg, reply_markup=None, **kwargs):
        reply_markup = reply_markup if reply_markup is None else reply_markup
        self.updater.bot.send_message(chat_id=update.message.chat_id,
                                      text=msg,
                                      reply_markup=reply_markup,
                                      **kwargs)

    def user_info(self, update):
        user = update.message.from_user
        try:
            name = user['first_name'] + ' ' + user['last_name']
        except:
            name = "Имя неизвестно"
        username = user["username"]
        return username, name

    def cancel(self, update, context):
        return ConversationHandler.END


if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()
