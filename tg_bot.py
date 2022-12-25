#!/usr/bin/python
# -*- coding: utf-8 -*-

from telegram import *
from telegram.ext import *
import coloredlogs, logging
from datetime import timedelta, datetime, time
import json
from random import randint

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


class TelegramBot:
    def __init__(self):
        # token = '1111327991:AAEfAijEz68wdHdVwFL53LYeuWVf9vuypTY'  # test bot
        token = '5562371099:AAE-s2UU7w6QbQCV9lCubBLVWHjpb4QMAC0'

        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.job_queue = JobQueue()

        self.tmp_data = {}
        with open("job.json") as file:
            self.job = json.load(file)
        print(self.job)
        for chat_id in self.job:
            first = str_to_time(self.job[chat_id]) - datetime.now()
            self.updater.job_queue.run_repeating(self.start, interval=timedelta(weeks=2),
                                                 first=first,
                                                 context=chat_id)
            self.updater.job_queue.start()

        text_filter = ~Filters.command(False)

        self.dispatcher.add_handler(CommandHandler('start', self.weekly_job, pass_job_queue=True))
        self.dispatcher.add_handler(CommandHandler('chat_id', self.chat_id))
        self.dispatcher.add_handler(
            ConversationHandler(
                entry_points=[MessageHandler(Filters.regex('Давай по классике, вдарим красного'), self.send_to_courier,
                                             pass_job_queue=True),
                              MessageHandler(Filters.regex('Давай лёгонького беленького'), self.send_to_courier,
                                             pass_job_queue=True),
                              MessageHandler(Filters.regex('Ой, хочется пузырёчков'), self.send_to_courier,
                                             pass_job_queue=True),
                              MessageHandler(Filters.regex('Вино красненькое'), self.send_to_courier,
                                             pass_job_queue=True),
                              MessageHandler(Filters.regex('К чёрту вино'), self.send_to_courier,
                                             pass_job_queue=True),
                              MessageHandler(Filters.regex('Вино беленькое'), self.send_to_courier,
                                             pass_job_queue=True),
                              MessageHandler(Filters.regex('Пивас-деребас'), self.send_to_courier,
                                             pass_job_queue=True),
                              MessageHandler(Filters.regex('Мальчик, водочки нам принеси'), self.send_to_courier,
                                             pass_job_queue=True)],
                states={},
                fallbacks=[CommandHandler("cancel", self.start),
                           MessageHandler(Filters.regex("Назад"), self.start)]))
        self.dispatcher.add_handler(MessageHandler(text_filter, self.send_non_msg))

        coloredlogs.install()
        # dispatcher.add_error_handler(lambda update, context, error: print(f'ERROR OCCURRED: {error}'))

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

    def weekly_job(self, update, context: CallbackContext):
        print(update.message.chat_id)
        if str(update.message.chat_id) in self.job.keys():
            return ConversationHandler.END
        self.send_message(update, "Ира, привет! Я телеграмный бот, и да, я - твой подарок на день рождения. Я умею дарить радость. Ну, не постоянно, конечно, а раз в две недели. Зато целый год! Да-да, я работаю до 16 ноября 2023 года. А потом уйду в закат.\n"
                                  "Дарить радость можно по-разному. Так вот, каждые две недели я буду сам сочинять для тебя вульгарные матерные анекдоты! Ну как? Рада? Знаааю, ты всегда такое хотела, шалунья, теперь будешь каждый раз ждать новый пошленький анектодик от меня!\n"
                                  "Возможно, ты уже успела понять, что я бот с юмором. Ха-ха-ха (компьютерным голосом). Нет, я не буду сочинять для тебя анекдоты, хотя я умею, обращайся, если станет скучно.\n"
                                  "Я буду возить тебе вино. Каждую вторую пятницу. В году примерно 52 недели, так что 26 порций ждет тебя. Порций, а не бутылок, да-да. Ты можешь иногда, когда сииильно весело или оооочень грустно, получить по две штуки. Ну, не обижайся, если вторая окажется портвешком, я всё-таки еврей.\n"
                                  "Что тебе надо делать? Отвечать по четвергам перед долгожданной Великой Доставочной Пятницей на мои вопросы. Их будет немного. Да, я задаю вопросы заранее, ведь мне надо еще вырастить виноград, собрать его, подавить его в бочке моими ботовскими ногами (а это сложно), и налить в бутылку получившийся великолепный напиток. Бутылка будет в пятницу материализовываться у тебя под дверью. Сама.  Да, я маг и волшебник. Кстати, можешь заказывать и не вино. Ну, вдруг заскучаешь по русской беленькой.\n"
                                  "В общем, пользуйся мной как хочешь. Мне можно писать в свободной форме что хочешь и когда хочешь. Но по доставке - жди  вопросов. Так что дерзай. Рррррррр.")
        first = datetime(year=2022, month=11, day=17, hour=23, minute=0)
        self.job[update.message.chat_id] = time_to_str(first)
        json.dump(self.job, open('job.json', 'w'))
        context.job_queue.run_repeating(self.start, interval=timedelta(weeks=2),
                                        first=first - datetime.now(),
                                        context=update.message.chat_id)
        context.job_queue.start()
        return ConversationHandler.END

    def start(self, context):
        chat_id = context.job.context
        first = str_to_time(self.job[chat_id])
        first += timedelta(weeks=2)
        self.job[chat_id] = time_to_str(first)
        json.dump(self.job, open('job.json', 'w'))
        ### добавить проверку на пользователя
        if randint(1, 3) == 1:
            keyboard = [
                ['Давай по классике, вдарим красного'],
                ['Давай лёгонького беленького'],
                ['Ой, хочется пузырёчков'],
                ['К чёрту вино']
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard)
            self.updater.bot.send_message(chat_id=chat_id, text="Эта пятница не обойдётся без вина. Какое?",
                                          reply_markup=reply_markup)
        else:
            keyboard = [
                ['Вино красненькое'],
                ['Вино беленькое'],
                ['Пивас-деребас'],
                ['Мальчик, водочки нам принеси']
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard)
            self.updater.bot.send_message(chat_id=chat_id, text="Ну-ка мечи стаканы на стол. Подо что стаканы?",
                                          reply_markup=reply_markup)
        return 1

    def send_to_courier(self, update, context):
        self.reply = update.message.text
        context.bot.send_message(chat_id=460209939, text=f"Сегодня Ирина хочет {self.reply}")
        context.bot.send_message(chat_id=363972614, text=f"Сегодня Ирина хочет {self.reply}")
        self.send_message(update, "Ира, ты сделала свой выбор. Смиренно ожидай")
        return ConversationHandler.END

    def chat_id(self, update, context):
        print(update.message.chat_id)
        return ConversationHandler.END

    def send_non_msg(self, update, context):
        msg = update.message.text
        if update.message.chat_id == 460209939 or update.message.chat_id == 316284874 or \
                update.message.chat_id == 363972614:
            context.bot.send_message(chat_id=581960599, text=msg)
        context.bot.send_message(chat_id=460209939, text=msg)
        context.bot.send_message(chat_id=316284874, text=msg)
        context.bot.send_message(chat_id=363972614, text=msg)
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
