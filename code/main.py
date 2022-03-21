import telebot
import config
import storage
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


def show_climate_info(message):
    keyb2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Вывести")
    item2 = types.KeyboardButton("Не выводить")
    keyb2.add(item1, item2)
    bot.send_message(message.chat.id, "Вывести информацию?", reply_markup=keyb2)


def climate_info_shell(id, chat_id):
    res = storage.climate_inform(id)
    for elem in res:
        bot.send_message(chat_id, str(elem['id']) + " " + elem['tur_month'],
                         reply_markup=types.ReplyKeyboardRemove())


def info_info_shell(id, chat_id):
    res = storage.info_inform(id)
    for elem in res:
        bot.send_message(chat_id, str(elem['id']) + " " + elem['capital'] + " " + elem['image'],
                         reply_markup=types.ReplyKeyboardRemove())
        bot.send_photo(chat_id, open(elem['image'], "rb"))


def menu():
    keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Информация о стране")
    item2 = types.KeyboardButton("Информация о климате")
    item3 = types.KeyboardButton("Справка")
    keyb.add(item1, item2, item3)
    return keyb


def instruction(chat_id):
    bot.send_message(chat_id, "Бот-турагент поможет узнать необходимую информацию.\n"
                              "Чтобы узнать различные сведения о странах нажмите на кнопку 'Информация о стране'.\n"
                              "Чтобы узнать сведения о климате стран нажмите на кнопку 'Информация о климате'.")


def country_keyb():
    keyi = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Испания", callback_data='Испания')
    item2 = types.InlineKeyboardButton("Греция", callback_data='Греция')
    item3 = types.InlineKeyboardButton("Объединенные Арабские Эмираты", callback_data='Объединенные Арабские Эмираты')
    item4 = types.InlineKeyboardButton("Индонезия", callback_data='Индонезия')
    item5 = types.InlineKeyboardButton("Мексика", callback_data='Мексика')
    keyi.add(item1, item2, item3, item4, item5)
    return keyi


def process_message(message):
    if message.text == "Да, начинаем":
        keyb_menu = menu()
        bot.send_message(message.chat.id, "Начинаем!\n"
                                          "Главное меню", parse_mode='html', reply_markup=keyb_menu)
        # show_climate_info(message)
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Ждем Вас снова!", parse_mode='html',
                         reply_markup=types.ReplyKeyboardRemove())
    elif message.text == "Справка":
        instruction(message.chat.id)
    elif message.text == "Информация о стране":
        keyb_i = country_keyb()
        bot.send_message(message.chat.id, "Выбирите страну из списка", reply_markup=keyb_i)

    else:
        bot.send_message(message.chat.id, "Извините, я не понимаю")
        # info_info_shell(message.text, message.chat.id)
        # bot.send_message(message.chat.id, "Учусь ...")


@bot.message_handler(commands=['start'])
def bot_start(message):
    bot.send_message(message.chat.id, "Здравствуйте, {0.first_name}!\n"
                                      "Я - {1.first_name}, бот - турагент "
                                      "Всегда готов помочь.".format(message.from_user, bot.get_me()), parse_mode='html')

    keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Да, начинаем")
    item2 = types.KeyboardButton("Нет")
    keyb.add(item1, item2)

    bot.send_message(message.chat.id, "Хотите начать ?",
                     parse_mode='html', reply_markup=keyb)


@bot.message_handler(content_types=['text'])
def message_in(message):
    process_message(message)

@bot.callback_query_handler(func=lambda call:True)
def callback_country(call):
    if call.data == 'Испания':
        bot.send_message(call.message.chat.id, "Вы выбрали Испанию")
    elif call.data == 'Греция':
        bot.send_message(call.message.chat.id, "Вы выбрали Грецию")
    elif call.data == 'Объединенные Арабские Эмираты':
        bot.send_message(call.message.chat.id, "Вы выбрали Объединенные Арабские Эмираты")
    elif call.data == 'Индонезия':
        bot.send_message(call.message.chat.id, "Вы выбрали Индонезию")
    elif call.data == 'Мексика':
        bot.send_message(call.message.chat.id, "Вы выбрали Мексику")

    res = storage.find_info_by_name(call.data)
    for elem in res:
        bot.send_message(call.message.chat.id, "Столица - " + elem['capital'] + ".\n" + "Население: " +
                         str(elem['population']) + " миллионов.\n" + elem['descr'])
        bot.send_photo(call.message.chat.id, open(elem['image'], "rb"))


bot.polling(none_stop=True)
