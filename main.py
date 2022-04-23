import telebot
from multiprocessing import *
import time

from get_status import get_status

bot = telebot.TeleBot('1957915766:AAFMZqJIT9aW1YNU0Dpb-zWeiswwTVP9-uI')
id = None


def proc_start():
    p_to_start = Process(target=start_schedule, args=(id,))
    p_to_start.start()
    return p_to_start


def proc_stop(p_to_stop):
    p_to_stop.terminate()


def start_schedule(id):
    while True:
        if id is not None:
            status = get_status(id)
            if status[0] == 'Online':
                bot.send_message('753613553', '''Пользователь <b><i>{0}</i></b> онлайн!'''.format(status[1]),
                                 parse_mode='html')
                time.sleep(60 * 10)
            else:
                time.sleep(60 * 5)
        else:
            bot.send_message('753613553', 'Цель отсутствует! (/target)',
                             parse_mode='html')
            time.sleep(60)


@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.send_message(msg.chat.id,
                     'Добро пожаловать, {0.first_name}, {1}!\nМеня зовут <b>"{2.first_name} - бот"</b>.'.format(
                         msg.from_user, msg.chat.id, bot.get_me()),
                     parse_mode='html')


@bot.message_handler(commands=['target'])
def target(msg):
    global id, pr
    id = msg.text.split('/target ')[1]
    if not id:
        bot.send_message(msg.chat.id, 'Пустое сообщение'.format(msg.text.split('/target ')[1]), parse_mode='html')
    else:
        status = get_status(id)
        if status != 'error':
            bot.send_message(msg.chat.id, 'Обновлена цель: {0}'.format(msg.text.split('/target ')[1]),
                             parse_mode='html')
            proc_stop(pr)
            pr = proc_start()

        else:
            bot.send_message(msg.chat.id,
                             '''Произошла ошибка: пользователь не найден или не удалось обработать запрос.''')
            id = None


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
    pr = proc_start()
    try:
        bot.polling(none_stop=True)
    except Exception:
        pass
