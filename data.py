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
daily_quiz = 'Ежедневный тест'
study = 'Хочу учиться!'
start = 'Старт'
cont = 'Продолжим!'
later = 'Давай позже'
ready = 'Понял!'
leaderboard = 'Список лидеров'
back = '<- Назад'

wanna_play = 'Хочешь поиграть ещё раз?'

back_keyboard = t.InlineKeyboardMarkup(row_width=2)
back_keyboard.row(t.InlineKeyboardButton(back, callback_data='back'))

lesson_keyboard = t.InlineKeyboardMarkup(row_width=2)
lesson_keyboard.row(t.InlineKeyboardButton(ready, callback_data='next_lesson'))

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
    ['lesson', '''Инфляция – рост цен на товары и услуги. При инфляции происходит обесценивание денег, снижается покупательная способность населения. Процесс, обратный инфляции, то есть снижение цен, называется дефляцией.
Простым языком — это когда деньги теряют свою цену. Например, если доллар начинает стоить больше рублей, значит произошла небольшая инфляция рубля по отношению к доллару. То есть мороженное за 10 рублей может стоить уже 20, потому что товар остался таким же, а деньги подешевели. Как то так.
По темпам роста цен инфляцию принято разделять на три вида.
Ползучая инфляция означает, что цены растут постепенно, приблизительно на 3-5% в год, как это происходит в развитых странах. Умеренная инфляция – положительный для экономики фактор, она стимулирует спрос, способствует расширению производства и инвестированию.
Галопирующая инфляция характерна для развивающихся стран. Рост цен составляет 10-50% в годовом исчислении.
При гиперинфляции рост цен превышает 50% и может достигать астрономических значений. Чаще всего возникает, когда государство «включает» печатный денежный станок для финансирования своих непомерных расходов.
К основным причинам возникновения инфляции относятся такие факторы:
- сокращение валового внутреннего продукта (ВВП) при неизменном объеме денежной массы в обращении;
- рост государственных расходов за счет эмиссии;
- чрезмерное расширение объемов кредитования компаний и частных лиц;
- монополизм в экономике, когда крупные фирмы получают возможность определять стоимость своей продукции и издержек.
'''],
    ['quiz', 'Основной причиной гиперинфляции является:',
     ('Резкое повышение валюты в обороте при неизменном ВВП', 'Именно так!'),
     ('Чрезмерное расширение объемов кредитования ',
      'Чаще всего [гиперинфляция] возникает, когда государство «включает» печатный денежный станок для финансирования своих непомерных расходов.'),
     (
     'Монополизм в экономике',
     'Чаще всего [гиперинфляция] возникает, когда государство «включает» печатный денежный станок для финансирования своих непомерных расходов.')],
    ['lesson', '''Волатильность – индикатор рынка ценных бумаг или валюты, показывающий уровень его изменчивости в определенный период.
Простым языком – это амплитуда колебания цен, разница между самой высокой и самой низкой ценой.
Волатильность измеряется в % от цены актива. 1-2% — это низкая волатильность, 10% и выше — большая волатильность.
Принято разделять историческую волатильность и ожидаемую, то есть прогнозируемую величину.
Значение волатильности дает возможность оценить риск вложений в тот или иной актив. Чем она выше, тем выше риск.'''],
    ['quiz', 'Формула волатильности:',
     ('Наибольшая цена за период - наименьшая цена за период', 'Правильно!'),
     ('Средняя цена за период', 'Нет, волатильность – это разница между самой высокой и самой низкой ценами.'),
     ('Наибольшая цена за период - средняя цена за период',
      'Нет, волатильность – это разница между самой высокой и самой низкой ценами.')]
]

# TODO: вопросы на daily quiz
questions = [
    # 1
    ['Как думаете, сколько стоила акция Амазона в декабре 2000-го года? Для справки: сейчас она стоит порядка 3100$.',
     ('89$', 'Это правильный ответ :)'),
     ('8$',
      'Акция Амазона стоила меньше 8$ с момента основания (июль 1994-го) по июнь 1998-го года. Правильный ответ – 89$'),
     ('34$', 'Близко, но в то время дела Амазона шли чуть лучше. Правильный ответ –  89$')],
    ['А в декабре 2006-го?',
     ('49$', 'Верно! Акции Амазона начали относительно стабильно расти только примерно в это время.'),
     ('178$', 'Неверно. Акции Амазона начали относительно стабильно расти только примерно с конца 2006-го года.'),
     ('272$', 'Неверно. Акции Амазона начали относительно стабильно расти только примерно с конца 2006-го года.')],
    ['Как думаете, сколько денег у вас будет к 55 годам, если инвестировать 25,000$ под 5$ годовых?',
     ('108,000$', 'Правильный ответ!'),
     ('54,000$', 'Нет. Правильный ответ в 2 раза больше.'),
     ('162,000$', 'Чуть-чуть перегнули! Правильный ответ – 108,000$')],
    ['Если бы вы вернулись в декабрь 2006-го, акции какой компании вы бы купили, если ваша цель – больше всего заработать к сентябрю 2020-го?',
     ('Amazon', 'Верно! Акции Амазона с того времени выросли примерно в 63 раза. Для сравнения: акции Apple выросли в 50 раз, в то время как акции Google подорожали всего в 6.5 раз.'),
     ('Apple', 'Почти верно. Акции Apple выросли в 50 раз, но акции Амазона – в целых 63! Акции Google подорожали всего в 6.5 раз.'),
     ('Google', 'Совсем неверно! Акции Google выросли всего в 6.5 раз, в то время как акции Amazon и Apple подорожали в 63 и 50 раз соответственно.')]

]


def last_words(score, name):
    return f'{name}, поздравляю, вы прошли ежедневный тест и набрали {score} баллов!'


with open('db.p', 'rb') as f:
    database = pickle.load(f)
