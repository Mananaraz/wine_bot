#!/usr/bin/python
# -*- coding: utf-8 -*-

from telegram import *
from telegram.ext import *
import coloredlogs, logging
from datetime import timedelta, datetime, time
import json

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


class TelegramBot:
    def __init__(self):
        token = '1111327991:AAEfAijEz68wdHdVwFL53LYeuWVf9vuypTY'  # test bot
        # token = '5562371099:AAE-s2UU7w6QbQCV9lCubBLVWHjpb4QMAC0'

        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.job_queue = JobQueue()

        self.tmp_data = {}
        with open("job.json") as file:
            self.job = json.load(file)
        for chat_id in self.job:
            first = str_to_time(self.job[chat_id]) - datetime.now()
            self.updater.job_queue.run_repeating(self.start, interval=timedelta(seconds=10),
                                        first=first,
                                        context=chat_id)
            self.updater.job_queue.start()

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
        self.updater.idle()

    def weekly_job(self, update, context: CallbackContext):
        # context.job_queue.run_repeating(self.start, interval=timedelta(weeks=1),
        #                                 first=datetime(year=2022, month=11, day=16,
        #                                                hour=1, minute=28) - datetime.now(),
        #                                 context=context)
        if update.message.chat_id in self.job.keys():
            return ConversationHandler.END
        self.send_message(update, "Ира, с днём рождения! А что умеет этот бот, ты узнаешь завтра")
        first = datetime(year=2022, month=11, day=16, hour=1, minute=28)
        self.job[update.message.chat_id] = time_to_str(first)
        json.dump(self.job, open('job.json', 'w'))
        context.job_queue.run_repeating(self.start, interval=timedelta(seconds=10),
                                        first=first - datetime.now(),
                                        context=update.message.chat_id)
        context.job_queue.start()
        return ConversationHandler.END

    def start(self, context):
        chat_id = context.job.context
        first = str_to_time(self.job[chat_id])
        first += timedelta(seconds=10)
        self.job[chat_id] = time_to_str(first)
        json.dump(self.job, open('job.json', 'w'))
        ### добавить проверку на пользователя
        keyboard = [
            ['Давай по классике, вдарим красного'],
            ['Давай лёгонького беленького'],
            ['Ой, хочется пузырёчков'],
            ['К чёрту вино']
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard)
        self.updater.bot.send_message(chat_id=chat_id, text="Эта пятница не обойдётся без вина. Какое?",
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


def time_to_str(time: datetime):
    return f'{time.year} {time.month} {time.day} {time.hour} {time.minute} {time.second}'


def str_to_time(string: str):
    year, month, day, hour, minute, second = [int(x) for x in string.split()]
    return datetime(year, month, day, hour, minute, second)


if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()
