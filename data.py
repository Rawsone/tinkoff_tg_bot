import pickle

from telebot import types as t

LEN = 1

TOKEN = '1348606409:AAGNX8GcOmwovJPUbfJ6sssARaoREcHwAp0'

welcome = 'Меня зовут Олег, я твой голосовой помощник. А как обращаться к тебе?'
##TODO:
greetings = 'Привет, {}. Предлагаю тебе '

when_ready = 'Хорошо, когда будешь готов, нажми "Старт"'

no_more_lessons = 'Молодец! Ты прошел все уроки на сегодня! Приходи завтра!'
quiz_done = 'Вы уже прошли ежедневний тест сегодня! Приходите завтра!'
not_yet = 'Еще не готов'
play = 'Играть!'
daily_quiz = 'Daily quiz!'
study = 'Хочу учиться!'
start = 'Старт'
cont = 'Продолжим!'
later = 'Давай позже'
ready = 'Готов!'
leaderboard = 'Список лидеров'

wanna_play = 'Хочешь поиграть ещё раз?'

lesson_keyboard = t.InlineKeyboardMarkup(row_width=2)
lesson_keyboard.row(t.InlineKeyboardButton(ready, callback_data='next_lesson'))

start_keyboard = t.InlineKeyboardMarkup(row_width=2)
start_keyboard.row(t.InlineKeyboardButton(ready, callback_data='start'))

cont_lesson_keyboard = t.InlineKeyboardMarkup(row_width=2)
cont_lesson_keyboard.row(t.InlineKeyboardButton(cont, callback_data='next_lesson'))

cont_keyboard = t.InlineKeyboardMarkup(row_width=2)
cont_keyboard.row(t.InlineKeyboardButton(cont, callback_data='next'))

wanna_play_keyboard = t.InlineKeyboardMarkup(row_width=2)
wanna_play_keyboard.row(t.InlineKeyboardButton(play, callback_data='play'))
wanna_play_keyboard.row(t.InlineKeyboardButton(later, callback_data='not_yet'))

# TODO: обучающий текст - маркер 'lesson'
# квиз по тексту - 'quiz'
# Первый элемент в tuple - вариант ответа,
# Второй элемент - объяснение для выбранного варианта
#
lessons = [
    ['lesson', 'l1'],
    ['quiz', 'Q1',
     ('Да', 'Молодец!'),
     ('Нет', 'Не молодец!')],
    ['lesson', 'l2'],
    ['quiz', 'Q2 ',
     ('Да', 'Молодец!'),
     ('Нет', 'Не молодец!')]
]

# TODO: вопросы на daily quiz
questions = [
    # 1
    ['Вопрос 1',
     ('Вариант ответа 1', 'Объяснение к варианту ответа 1'),
     ('Вариант ответа 2', 'Объяснение к варианту ответа 2'),
     ('Вариант ответа 3', 'Объяснение к варианту ответа 3')]
]


def last_words(score, name):
    if score > 5:
        return '{}, поздравляю, ты человек будущего, ты готов менять мир, нам с тобой по пути. ' \
               'Твоя эрудированность и целеустремленность позволят достигнуть успеха в ' \
               'любой профессиональной деятельности.'.format(name)
    elif score > 3:
        return '{}, поздравляю, ты на правильном пути. Я тебе дам пару ссылок. ' \
               'Думаю, тебе будет интересно узнать больше о возможностях ИИ и технологиях будущего.' \
               '\nhttps://sk.ru/news/iskusstvennyy-intellekt-v-sovremennom-iskusstve/' \
               '\nhttps://kanobu.ru/articles/iskusstvennyij-intellekt-buduschee-tsivilizatsii-ili-ee-ubijtsa-369258/' \
               '\nhttps://dtf.ru/science/41917-sovremennoe-sostoyanie-iskusstvennogo-intellekta '.format(name)

    return '{} - здорово, что ты интересуешься ИИ! ' \
           'Погугли, изучи вопрос подробнее и приходи, поиграем ещё раз.'.format(name)


with open('db.p', 'rb') as f:
    database = pickle.load(f)
