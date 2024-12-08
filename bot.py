import telebot
from ParserEdaRu import find_dish_on_website
import ParserOzon

remi = telebot.TeleBot('lala')  # the token

dish = ''
numb = 0
name = ''


@remi.message_handler(commands=['start'], content_types=['text'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn0 = telebot.types.KeyboardButton('Хочу что-то приготовить')
    help = telebot.types.KeyboardButton('Помощь')
    markup.add(btn0, help)
    remi.send_message(message.from_user.id, 'Привет! Я бот для готовки!', reply_markup=markup)
    remi.register_next_step_handler(message, new_dish)


@remi.message_handler(commands=['new_dish'], content_types=['text'])
def new_dish(message):
    if message.text == 'Хочу что-то приготовить':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton('да')
        btn2 = telebot.types.KeyboardButton('нет')
        back = telebot.types.KeyboardButton('Вернуться назад (в главное меню)')
        help = telebot.types.KeyboardButton('Помощь')
        markup.add(btn1, btn2, back, help)
        remi.send_message(message.from_user.id, 'Вы знаете, что хотите приготовить?', reply_markup=markup)
    elif message.text == 'Помощь':
        remi.send_message(message.from_user.id,
                          'Забыл представиться! Я - бот, который поможет тебе подобрать продукты для блюда и купить их, '
                          'попробуй написать мне, а я постараюсь помочь')
    remi.register_next_step_handler(message, do_user_know)


def do_user_know(message):
    if message.text == 'да':
        remi.send_message(message.from_user.id, 'Ура! Напишите мне название блюда, а я скину вам рецепт!')
        remi.register_next_step_handler(message, get_dish)  # следующий шаг – функция get_dish
    elif message.text == 'нет':
        print('todo')
        # todo with random
    elif message.text == 'Помощь':
        remi.send_message(message.from_user.id,
                          'Забыл представиться! Я - бот, который поможет тебе подобрать продукты для блюда и купить их, '
                          'попробуй написать мне, а я постараюсь помочь')
    elif message.text == 'Вернуться назад (в главное меню)':
        remi.register_next_step_handler(message, new_dish)


def get_dish(message):
    global dish
    dish = message.text
    if is_name_of_dish(dish):
        remi.register_next_step_handler(message, get_number_of_portions)
    else:
        remi.send_message(message.from_user.id, 'К сожалению, такого блюда еще нет :(, хотите попробовать еще раз?')
        # try ask again


def is_name_of_dish(name):
    # is the str7
    if not find_dish_on_website(name):
        return 0
    # found the name on the site
    else:
        remi.register_next_step_handler(name, get_number_of_portions)
    # if we found it, then go to prop


@remi.message_handler(commands=['portions'])
def get_number_of_portions(message):
    global numb
    numb = message.text()
    remi.send_message(message.from_user.id, 'Сколько вы хотите порций?')
    if numb.isnumeric:
        remi.register_next_step_handler(message, process)
    else:
        remi.send_message(message.from_user.id, 'Это не число :(, давайте попробуем еще раз')
        remi.register_next_step_handler(message, get_number_of_portions)


def process(n):
    print(n)
    # todo after we found the dish, need to get products, portions and amount


remi.polling(none_stop=True)
