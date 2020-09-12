import os
from random import sample, shuffle

import telebot

from data import *

bot = telebot.TeleBot(TOKEN)


def question_keyboard(num, question):
    kb = t.InlineKeyboardMarkup(row_width=1)

    qs = question[1:]

    keys = []
    for i, q in enumerate(qs):
        keys.append(t.InlineKeyboardButton(q[0], callback_data=f'ans_{num}_{i}'))

    shuffle(keys)
    kb.add(*keys)

    return kb


@bot.message_handler(commands=['start'])
def start(message: t.Message):
    if message.chat.id not in database:

        bot.send_message(message.chat.id, welcome)

        bot.register_next_step_handler(message, enter_name)

    else:
        start_msg(message)


def enter_name(message: t.Message):
    database[message.chat.id] = {'name': message.text.strip()}

    bot.send_message(message.chat.id,
                     greetings.format(message.text.strip()),
                     reply_markup=play_keyboard)


@bot.callback_query_handler(func=lambda c: c.data == 'not_yet')
def not_yet(call: t.CallbackQuery):
    bot.edit_message_text(when_ready,
                          call.message.chat.id,
                          call.message.message_id,
                          reply_markup=start_keyboard)


@bot.message_handler(commands=['play'])
def start_msg(message: t.Message):
    database[message.chat.id]['game'] = sample(range(len(questions)), LEN)
    database[message.chat.id]['game_score'] = 0

    message = bot.send_message(message.chat.id, 'Loading...')

    next_question(message)


@bot.callback_query_handler(func=lambda c: c.data == 'play')
def start(call: t.CallbackQuery):
    database[call.message.chat.id]['game'] = sample(range(len(questions)), LEN)
    database[call.message.chat.id]['game_score'] = 0

    next_question(call.message)


@bot.callback_query_handler(func=lambda c: c.data == 'next')
def next_question(call: t.CallbackQuery):
    message = call.message if isinstance(call, t.CallbackQuery) else call

    name = database[message.chat.id]['name']
    game = database[message.chat.id]['game']

    if game:
        num = game.pop()
        question = questions[num]

        print(name, 'отвечает на вопрос ', num + 1)

        bot.delete_message(message.chat.id, message.message_id)
        if os.path.isfile(f'media/{num + 1}-q.jpg'):
            with open(f'media/{num + 1}-q.jpg', 'rb') as f:
                bot.send_photo(message.chat.id, f, question[0].format(name),
                               reply_markup=question_keyboard(num, questions[num]))
        else:
            with open(f'media/{num + 1}-q.mp3', 'rb') as f:
                bot.send_audio(message.chat.id, f, question[0].format(name),
                               reply_markup=question_keyboard(num, questions[num]))

    else:
        score = database[message.chat.id]['game_score']

        bot.delete_message(message.chat.id, message.message_id)

        bot.send_message(message.chat.id,
                         last_words(score, name) + '\n\n' + wanna_play,
                         reply_markup=wanna_play_keyboard,
                         disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda c: c.data.startswith('ans'))
def answer(call: t.CallbackQuery):
    num, ans = map(int, call.data.split('_')[1:])

    name = database[call.message.chat.id]['name']

    print(name, 'ответил на вопрос ', num + 1, 'правильно' if ans == 0 else 'неправильно')

    database[call.message.chat.id]['game_score'] += int(ans == 0)

    bot.delete_message(call.message.chat.id, call.message.message_id)

    if os.path.isfile(f'media/{num + 1}-a.jpg'):
        with open(f'media/{num + 1}-a.jpg', 'rb') as f:
            bot.send_photo(call.message.chat.id, f, questions[num][ans + 1][1].format(name),
                           reply_markup=cont_keyboard)
    else:
        bot.send_message(call.message.chat.id,
                         questions[num][ans + 1][1].format(name),
                         reply_markup=cont_keyboard)


if __name__ == '__main__':
    try:
        database = {}
        print(database)
        bot.polling()
    except:
        pass
    finally:
        with open('db.p', 'wb') as f:
            pickle.dump(database, f)
