import os
from random import sample, shuffle

import telebot

from data import *

bot = telebot.TeleBot(TOKEN)


def play_keyboard(daily_quiz_done=False):
    play_keyboard = t.InlineKeyboardMarkup(row_width=2)
    if not daily_quiz_done:
        play_keyboard.add(t.InlineKeyboardButton(daily_quiz, callback_data='daily_quiz'))
    play_keyboard.add(t.InlineKeyboardButton(study, callback_data='study'))
    play_keyboard.add(t.InlineKeyboardButton(leaderboard, callback_data='leaderboard'))

    return play_keyboard


def question_keyboard(num, question, is_daily):
    kb = t.InlineKeyboardMarkup(row_width=1)

    qs = question[1:]

    keys = []
    suffix = 'daily' if is_daily else 'lesson'
    for i, q in enumerate(qs):
        keys.append(t.InlineKeyboardButton(q[0], callback_data=f'ans{suffix}_{num}_{i}'))

    # shuffle(keys)
    kb.add(*keys)

    return kb


@bot.callback_query_handler(func=lambda c: c.data == 'leaderboard')
def get_leaderboard(call):
    bot.send_message(call.message.chat.id, '\n'.join([f'{i + 1}) {user["name"]} - {user["daily_quiz_score"]} points' for i, user in
                                                 enumerate(
                                                     sorted(database.values(), key=lambda x: -x['daily_quiz_score']))]))


@bot.message_handler(commands=['start'])
def start(message: t.Message):
    if message.chat.id not in database:

        bot.send_message(message.chat.id, welcome)

        bot.register_next_step_handler(message, enter_name)

    else:
        name = database[message.chat.id]['name']
        bot.send_message(message.chat.id,
                         greetings.format(name),
                         reply_markup=play_keyboard('daily_quiz_done' in database[message.chat.id]))


def enter_name(message: t.Message):
    database[message.chat.id] = {'name': message.text.strip()}

    bot.send_message(message.chat.id,
                     greetings.format(message.text.strip()),
                     reply_markup=play_keyboard('daily_quiz_done' in database[message.chat.id]))


@bot.callback_query_handler(func=lambda c: c.data == 'not_yet')
def not_yet(call: t.CallbackQuery):
    bot.edit_message_text(when_ready,
                          call.message.chat.id,
                          call.message.message_id,
                          reply_markup=start_keyboard)


# @bot.message_handler(commands=['quiz'])
# def start_msg(message: t.Message):
#
#     database[message.chat.id]['game'] = sample(range(len(questions)), LEN)
#     database[message.chat.id]['daily_quiz_score'] = 0
#
#     message = bot.send_message(message.chat.id, 'Loading...')
#
#     next_question(message)

@bot.callback_query_handler(func=lambda c: c.data == 'study')
def start(call: t.CallbackQuery):
    database[call.message.chat.id]['lessons'] = list(range(len(lessons)))
    if 'study_score' not in database[call.message.chat.id]:
        database[call.message.chat.id]['study_score'] = 0

    next_lesson(call.message)


@bot.callback_query_handler(func=lambda c: c.data == 'daily_quiz')
def start_daily_quiz(call: t.CallbackQuery):
    if 'daily_quiz_done' not in database[call.message.chat.id]:
        database[call.message.chat.id]['daily_quiz_done'] = True
        database[call.message.chat.id]['game'] = sample(range(len(questions)), LEN)
        database[call.message.chat.id]['daily_quiz_score'] = 0

        next_question(call.message)
    else:
        bot.send_message(call.message.chat.id, quiz_done,
                         reply_markup=play_keyboard)


@bot.callback_query_handler(func=lambda c: c.data == 'next_lesson')
def next_lesson(call: t.CallbackQuery):
    message = call.message if isinstance(call, t.CallbackQuery) else call

    name = database[message.chat.id]['name']
    lessons_nums = database[message.chat.id]['lessons']

    if lessons_nums:
        num = lessons_nums.pop(0)
        lesson = lessons[num]
        bot.delete_message(message.chat.id, message.message_id)
        if lesson[0] == 'lesson':
            if os.path.isfile(f'media/{num + 1}-lq.jpg'):
                with open(f'media/{num + 1}-lq.jpg', 'rb') as f:
                    bot.send_photo(message.chat.id, f, lesson[1].format(name),
                                   reply_markup=lesson_keyboard)
            else:
                bot.send_message(message.chat.id, lesson[1].format(name),
                                 reply_markup=play_keyboard('daily_quiz_done' in database[message.chat.id]))
        else:
            if os.path.isfile(f'media/{num + 1}-q.jpg'):
                with open(f'media/{num + 1}-q.jpg', 'rb') as f:
                    bot.send_photo(message.chat.id, f, lesson[1].format(name),
                                   reply_markup=question_keyboard(num, lessons[num][1:], is_daily=False))
            else:
                bot.send_message(message.chat.id, lesson[1].format(name),
                                 reply_markup=question_keyboard(num, lessons[num][1:], is_daily=False))

    else:

        bot.delete_message(message.chat.id, message.message_id)

        bot.send_message(message.chat.id,
                         no_more_lessons,
                         reply_markup=play_keyboard('daily_quiz_done' in database[message.chat.id]),
                         disable_web_page_preview=True)


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
        if os.path.isfile(f'media/{num + 1}-dq.jpg'):
            with open(f'media/{num + 1}-dq.jpg', 'rb') as f:
                bot.send_photo(message.chat.id, f, question[0].format(name),
                               reply_markup=question_keyboard(num, questions[num], is_daily=True))
        else:
            bot.send_message(message.chat.id, question[0].format(name),
                           reply_markup=question_keyboard(num, questions[num], is_daily=True))

    else:
        score = database[message.chat.id]['daily_quiz_score']

        bot.delete_message(message.chat.id, message.message_id)

        bot.send_message(message.chat.id,
                         last_words(score, name) + '\n\n' + wanna_play,
                         reply_markup=play_keyboard('daily_quiz_done' in database[message.chat.id]),
                         disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda c: c.data.startswith('anslesson'))
def answer(call: t.CallbackQuery):
    num, ans = map(int, call.data.split('_')[1:])  # noqa

    name = database[call.message.chat.id]['name']

    print(name, 'ответил на вопрос ', num + 1, 'правильно' if ans == 0 else 'неправильно')

    database[call.message.chat.id]['study_score'] += int(ans == 0)

    bot.delete_message(call.message.chat.id, call.message.message_id)

    if os.path.isfile(f'media/{num + 1}-a.jpg'):
        with open(f'media/{num + 1}-a.jpg', 'rb') as f:
            bot.send_photo(call.message.chat.id, f, lessons[num][ans + 2][1].format(name),
                           reply_markup=cont_lesson_keyboard)
    else:
        bot.send_message(call.message.chat.id,
                         questions[num][ans + 2][1].format(name),
                         reply_markup=cont_lesson_keyboard)


@bot.callback_query_handler(func=lambda c: c.data.startswith('ansdaily'))
def answer(call: t.CallbackQuery):
    num, ans = map(int, call.data.split('_')[1:])

    name = database[call.message.chat.id]['name']

    print(name, 'ответил на вопрос ', num + 1, 'правильно' if ans == 0 else 'неправильно')

    database[call.message.chat.id]['daily_quiz_score'] += int(ans == 0)

    bot.delete_message(call.message.chat.id, call.message.message_id)

    if os.path.isfile(f'media/{num + 1}-da.jpg'):
        with open(f'media/{num + 1}-da.jpg', 'rb') as f:
            bot.send_photo(call.message.chat.id, f, questions[num][ans + 1][1].format(name),
                           reply_markup=cont_keyboard)
    else:
        bot.send_message(call.message.chat.id,
                         questions[num][ans + 1][1].format(name),
                         reply_markup=cont_keyboard)


if __name__ == '__main__':
    try:
        # database = {}
        print(database)
        bot.polling()
    except:
        pass
    finally:
        with open('db.p', 'wb') as f:
            pickle.dump(database, f)
