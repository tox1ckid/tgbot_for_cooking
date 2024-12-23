import telebot
from ParserEdaRu import find_dish_on_website, calculate
from ParserOzon import get_products_links

# remy is the name of the bot (mouse in Ratatouille)
remy = telebot.TeleBot('LALALA')  # the token

text_help = 'Я - бот, который поможет тебе подобрать продукты для блюда и купить их, ' \
            'попробуй написать мне, а я постараюсь помочь, вот мои команды: ' \
            '\n /start - для начала работы' \
            '\n /help - вызов помощи (этого сообщения) ' \
            '\n /main_menu - перейти в главное меню '


@remy.message_handler(commands=['main_menu'])
def main_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn0 = telebot.types.KeyboardButton('Хочу что-то приготовить')
    help = telebot.types.KeyboardButton('Помощь')
    markup.add(btn0, help)
    return markup


@remy.message_handler(commands=['start'])
def start(message):
    if message.text[0] == '/':
        match message.text:
            case '/help':
                remy.send_message(message.from_user.id, text_help)
                remy.register_next_step_handler(message, start)
            case '/main_menu':
                remy.register_next_step_handler(message, main_menu(message))
                remy.register_next_step_handler(message, new_dish)

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn0 = telebot.types.KeyboardButton('Хочу что-то приготовить')
    help = telebot.types.KeyboardButton('Помощь')
    markup.add(btn0, help)
    remy.send_message(message.from_user.id, 'Привет! Я бот для готовки!', reply_markup=markup)
    remy.register_next_step_handler(message, new_dish)


@remy.message_handler(commands=['new_dish'])
def new_dish(message):
    if message.text[0] == '/':
        match message.text:
            case '/start':
                start(message)
            case '/help':
                remy.send_message(message.from_user.id, text_help)
                remy.register_next_step_handler(message, new_dish)
            case '/main_menu':
                remy.send_message(chat_id=message.chat.id, text='Вы вернулись в главное меню',
                                  reply_markup=main_menu(message))
                remy.register_next_step_handler(message, new_dish)

    if message.text == 'Хочу что-то приготовить':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton('да')
        btn2 = telebot.types.KeyboardButton('нет')
        back = telebot.types.KeyboardButton('В главное меню')
        help = telebot.types.KeyboardButton('Помощь')
        markup.add(btn1, btn2, back, help)
        remy.send_message(message.from_user.id, 'Вы знаете, что хотите приготовить?', reply_markup=markup)
        remy.register_next_step_handler(message, do_user_know)
    elif message.text == 'Помощь':
        remy.send_message(message.from_user.id, text_help)
        remy.register_next_step_handler(message, new_dish)


def do_user_know(message):
    if message.text[0] == '/':
        match message.text:
            case '/start':
                start(message)
            case '/help':
                remy.send_message(message.from_user.id, text_help)
                remy.register_next_step_handler(message, do_user_know)
            case '/main_menu':
                remy.send_message(chat_id=message.chat.id, text='Вы вернулись в главное меню',
                                  reply_markup=main_menu(message))
                remy.register_next_step_handler(message, new_dish)

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = telebot.types.KeyboardButton('В главное меню')
    help = telebot.types.KeyboardButton('Помощь')
    markup.add(back, help)

    if message.text == 'да':
        remy.send_message(message.from_user.id, 'Ура! Напишите мне название блюда, а я скину вам рецепт!',
                          reply_markup=markup)
        remy.register_next_step_handler(message, get_dish)  # следующий шаг – функция get_dish
    elif message.text == 'нет':
        remy.send_message(message.from_user.id, 'Пока в разработке :(')
        # todo with random
    elif message.text == 'Помощь':
        remy.send_message(message.from_user.id, text_help)
        remy.register_next_step_handler(message, do_user_know)
    elif message.text == 'В главное меню':
        remy.send_message(chat_id=message.chat.id, text='Вы вернулись в главное меню', reply_markup=main_menu(message))
        remy.register_next_step_handler(message, new_dish)


@remy.message_handler(commands=['get_dish'])
def get_dish(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = telebot.types.KeyboardButton('В главное меню')
    help = telebot.types.KeyboardButton('Помощь')
    markup.add(back, help)
    if message.text[0] == '/':
        match message.text:
            case '/start':
                start(message)
            case '/help':
                remy.send_message(message.from_user.id, text_help)
                remy.register_next_step_handler(message, get_dish)
            case '/main_menu':
                remy.send_message(chat_id=message.chat.id, text='Вы вернулись в главное меню',
                                  reply_markup=main_menu(message))
                remy.register_next_step_handler(message, new_dish)

    global dish
    dish = message.text
    if message.text == 'Помощь':
        remy.send_message(message.from_user.id, text_help)
        remy.register_next_step_handler(message, get_dish)
    elif message.text == 'В главное меню':
        remy.send_message(chat_id=message.chat.id, text='Вы вернулись в главное меню', reply_markup=main_menu(message))
        remy.register_next_step_handler(message, new_dish)
    elif dish[0] == '/':
        a = 1
    elif is_name_of_dish(dish):
        remy.send_message(message.from_user.id, 'Сколько вы хотите порций?', reply_markup=markup)
        remy.register_next_step_handler(message, get_number_of_portions, dish)
    else:
        remy.send_message(message.from_user.id, 'К сожалению, такого блюда еще нет :(, хотите попробовать еще раз? '
                                                'Я верну вас в главное меню')
        remy.send_message(chat_id=message.chat.id, text='Вы вернулись в главное меню', reply_markup=main_menu(message))
        remy.register_next_step_handler(message, new_dish)
        # try ask again


def is_name_of_dish(name):
    return find_dish_on_website(name)[0] != 0
    # if we found it


@remy.message_handler(commands=['portions'])
def get_number_of_portions(message, requested_dish):
    if message.text[0] == '/':
        match message.text:
            case '/start':
                start(message)
            case '/help':
                remy.send_message(message.from_user.id, text_help)
                remy.register_next_step_handler(message, get_number_of_portions)
            case '/main_menu':
                remy.send_message(chat_id=message.chat.id, text='Вы вернулись в главное меню',
                                  reply_markup=main_menu(message))
                remy.register_next_step_handler(message, new_dish)
    global numb
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = telebot.types.KeyboardButton('В главное меню')
    help = telebot.types.KeyboardButton('Помощь')
    markup.add(back, help)
    numb = message.text

    if message.text == 'Помощь':
        remy.send_message(message.from_user.id, text_help)
        remy.register_next_step_handler(message, get_number_of_portions)
    elif message.text == 'В главное меню':
        remy.send_message(chat_id=message.chat.id, text='Вы вернулись в главное меню', reply_markup=main_menu(message))
        remy.register_next_step_handler(message, new_dish)
    elif numb.isnumeric:
        [ingredients, measures, links_products] = process(numb, requested_dish)
        reply = 'Вот список продуктов:\n'

        for i in range(len(ingredients)):
            current = f'{ingredients[i]}, {" ".join(str(j) for j in measures[i])}, {links_products[i]}\n'
            reply += current
        reply += '\nУдачного кулинарного опыта!!! Зовите, если снова понадоблюсь! Отправляю вас в главное меню'
        remy.send_message(message.from_user.id, reply, reply_markup=main_menu(message))
        remy.register_next_step_handler(message, new_dish)
    else:
        remy.send_message(message.from_user.id, 'Это не число :(, давайте попробуем еще раз, введите число на этот раз')
        remy.register_next_step_handler(message, get_number_of_portions, requested_dish)


def process(amount, requested_dish):
    amount = int(amount)
    [ingredients, measures] = find_dish_on_website(requested_dish)
    measures = calculate(amount, measures)
    links_products = []

    for i in ingredients:
        links_products.append(get_products_links(i))

    return [ingredients, measures, links_products]


remy.polling(none_stop=True)
