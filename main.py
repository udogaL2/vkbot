import telebot
from multiprocessing import *
import time

from get_status import get_status

bot = telebot.TeleBot('1957915766:AAFMZqJIT9aW1YNU0Dpb-zWeiswwTVP9-uI')


def start_process():
    p1 = Process(target=P_schedule.start_schedule, args=())
    p1.start()


class P_schedule():
    def start_schedule():
        while True:
            id = 'ka.terinass'
            status = get_status(id)
            if status[0] == 'Online':
                bot.send_message('753613553', '''Пользователь <b><i>{0}</i></b> онлайн!'''.format(status[1]),
                                 parse_mode='html')
                time.sleep(60 * 10)
            else:
                time.sleep(60 * 5)


@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.send_message(msg.chat.id,
                     'Добро пожаловать, {0.first_name}, {1}!\nМеня зовут <b>"{2.first_name} - бот"</b>.'.format(
                         msg.from_user, msg.chat.id, bot.get_me()),
                     parse_mode='html')


@bot.message_handler(content_types=['text'])
def give_status(msg):
    if msg.chat.id == 753613553:
        id = msg.text
        status = get_status(id)

        if status != 'error':
            bot.send_message('753613553',
                             '''Статус для пользователя <b><i>{0}</i></b> ({1}):\n"<i>{2}</i>" (время МСК)'''.format(
                                 status[1], id, status[0]), parse_mode='html')
        else:
            bot.send_message('753613553',
                             '''Произошла ошибка: пользователь не найден или не удалось обработать запрос.''')
    else:
        bot.send_message(msg.chat.id, 'Доступ запрещен!')


if __name__ == '__main__':
    start_process()
    try:
        bot.polling(none_stop=True)
    except Exception:
        pass
