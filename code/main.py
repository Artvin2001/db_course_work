import telebot
import config

import climate
import DataAccess
from telebot import types
import keyboards
import headlines
import facade
import generate_users
import storage


bot = telebot.TeleBot(config.TOKEN)
facade = facade.Facade()


def check_data_shell(logini, passwordi):
    permissioni = 3
    elem = facade.user_rep.check_user_data(logini, passwordi)
    for el in elem:
        permissioni = el.permission
    return permissioni


def one_more_time_keyb():
    keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Еще раз")
    keyb.add(item1)
    return keyb


def register():
    keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Уже зарегистрирован")
    item2 = types.KeyboardButton("Еще не зарегистрирован")
    keyb.add(item1, item2)
    return keyb

#to do
def instruction(chat_id):
    bot.send_message(chat_id, "Бот-турагент поможет узнать необходимую информацию.\n"
                              "Чтобы узнать различные сведения нажмите на кнопку 'Информация о ...'.\n"
                              "Чтобы изменить информацию нажмите на кнопку 'Изменить ...'.\n"
                              "Чтобы добавить что-то нажмите на кнопку 'Добавить ...'.\n"
                              "Чтобы удалить что-то нажмите на кнопку 'Удалить ...'.\n"
                              "Для выхода нажмите на кнопку 'Выход' или введите команду /stop.")


def yes_no():
    keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Да")
    item2 = types.KeyboardButton("Нет")
    keyb.add(item1, item2)
    return keyb

def sort_names(res):
    names = []
    for elem in res:
        names.append(elem.name)

    for i in range(len(names) - 1):
        for j in range(len(names) - i - 1):
            if names[j] > names[j + 1]:
                names[j], names[j + 1] = names[j + 1], names[j]
    return names

def keyb_new(res):
    keyc = types.InlineKeyboardMarkup(row_width=1)
    items = []
    names = sort_names(res)
    for elem in names:
        item = types.InlineKeyboardButton(elem, callback_data=elem)
        items.append(item)
    for i in items:
        keyc.add(i)
    return keyc


def hotel_keyb(res):
    keyi = types.InlineKeyboardMarkup(row_width=1)

    for elem in res:
        item = types.InlineKeyboardButton(elem.name + ' ' +  str(elem.stars) + '*', callback_data=elem.name)
        keyi.add(item)

    return keyi




@bot.message_handler(commands=['start'])
def bot_start(message):
    bot.send_message(message.chat.id, "Здравствуйте, {0.first_name}!\n"
                                      "Я - {1.first_name}, бот - турагент "
                                      "Всегда готов помочь.".format(message.from_user, bot.get_me()), parse_mode='html')

    keyb = yes_no()

    bot.send_message(message.chat.id, "Хотите начать ?",
                     parse_mode='html', reply_markup=keyb)


@bot.message_handler(content_types=['text'])
def message_in(message):
    if message.text == "Да":
        keyb_reg = register()
        bot.send_message(message.chat.id, "Вы уже зарегистрированы?", reply_markup=keyb_reg)
        bot.register_next_step_handler(message, have_registered)
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Ждем Вас снова!", parse_mode='html',
                         reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, bot_start)
    else:
        keyb_reg = register()
        bot.send_message(message.chat.id, "Сеанс был завершен, войдите в систему или зарегистрируйтесь", reply_markup=keyb_reg)
        bot.register_next_step_handler(message, have_registered)

def have_registered(message):
    if message.text == "Еще не зарегистрирован":
        bot.send_message(message.chat.id, "Введите Ваш логин")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.chat.id, "Введите Ваш логин для входа")
        bot.register_next_step_handler(message, get_login)

def get_name(message):
    if len(message.text) <= 30:
        facade.user.set_login(message.text)
        elem = facade.user_rep.check_user_login(facade.user.login)
        if elem:
            bot.send_message(message.chat.id, "Этот логин недоступен")
            bot.send_message(message.chat.id, "Введите логин для входа")
            bot.register_next_step_handler(message, get_name)
        else:
            bot.send_message(message.chat.id, "Введите пароль")
            bot.register_next_step_handler(message, get_password)
    else:
        bot.send_message(message.chat.id, "Некорректный логин, попробуйте ввести логин еще раз")
        bot.register_next_step_handler(message, get_name)

def get_login(message):
    if len(message.text) <= 30:
         facade.user.set_login(message.text)
         bot.send_message(message.chat.id, "Введите Ваш пароль для входа")
         bot.register_next_step_handler(message, check_login_pass)
    else:
        bot.send_message(message.chat.id, "Некорректный логин, попробуйте ввести логин еще раз")
        bot.register_next_step_handler(message, get_login)

def check_login_pass(message):
    facade.user.set_password(message.text)
    facade.user.set_permission(check_data_shell(facade.user.login, facade.user.password))

    if facade.user.permission == 3:
        keyb_more = one_more_time_keyb()
        bot.send_message(message.chat.id, "Неверный логин или пароль, попробуйте еще раз", reply_markup=keyb_more)
        bot.register_next_step_handler(message, message_in)
    else:
        facade.id = facade.user_rep.get_user_id(facade.user.login)
        facade.menu_keyb()
        #change context
        facade.country_rep.change_context(facade.user.login, facade.user.password)
        facade.climate_rep.change_context(facade.user.login, facade.user.password)
        facade.city_rep.change_context(facade.user.login, facade.user.password)
        facade.hotel_rep.change_context(facade.user.login, facade.user.password)
        facade.room_rep.change_context(facade.user.login, facade.user.password)
        facade.user_rep.change_context(facade.user.login, facade.user.password)
        storage.new_context(facade.user.login, facade.user.password)
        bot.send_message(message.chat.id, "Начинаем!\n"
                                          "Главное меню", parse_mode='html', reply_markup=facade.keyb)
        bot.register_next_step_handler(message, process_message)


def get_password(message):
    if len(message.text) <= 20:
        facade.user.set_password(message.text)
        elem = facade.user_rep.check_user_password(facade.user.password)
        if elem:
            bot.send_message(message.chat.id, "Этот пароль недоступен")
            bot.send_message(message.chat.id, "Введите пароль для входа")
        else:
            bot.send_message(message.chat.id, "Напишите какими правами доступа будет обладать данный аккаунт (Админимcтратор/Модератор/Пользователь). "
                                              "По умолчанию Вам могут быть выданы права пользователя.")
            bot.register_next_step_handler(message, get_permission)
    else:
        bot.send_message(message.chat.id, "Некорректный пароль, попбробуйте ввести пароль еще раз")
        bot.register_next_step_handler(message, get_password)

def add_perm(message):
    if message.text == 'Администратор' or message.text == 'администратор':
        perm = 0
    elif message.text == 'Модератор' or message.text == 'модератор':
        perm = 1
    else:
        perm = 2

    facade.user_rep.insert_user(facade.user.login, facade.user.password, perm)
    bot.send_message(message.chat.id, "Пользователь добавлен")
    facade.menu_keyb()
    # change context
    facade.country_rep.change_context(facade.user.login, facade.user.password)
    facade.climate_rep.change_context(facade.user.login, facade.user.password)
    facade.city_rep.change_context(facade.user.login, facade.user.password)
    facade.hotel_rep.change_context(facade.user.login, facade.user.password)
    facade.room_rep.change_context(facade.user.login, facade.user.password)
    facade.user_rep.change_context(facade.user.login, facade.user.password)
    storage.new_context(facade.user.login, facade.user.password)
    bot.send_message(message.chat.id, "Главное меню",
                     reply_markup=facade.keyb)
    bot.register_next_step_handler(message, process_message)

def get_permission(message):
    if message.text == 'Администратор' or message.text == 'администратор':
        facade.user.permission = 0
    elif message.text == 'Модератор' or message.text == 'модератор':
        facade.user.permission = 1
    else:
        facade.user.permission = 2
    try:
         bot.send_message(message.chat.id, "Регистрируем")
         facade.user_rep.insert_user(facade.user.login, facade.user.password, facade.user.permission)
         facade.id = facade.user_rep.get_user_id(facade.user.login)
         bot.send_message(message.chat.id, "Вы зарестрированы")
         facade.menu_keyb()
         bot.send_message(message.chat.id, "Начинаем!\n"
                                        "Главное меню", parse_mode='html', reply_markup=facade.keyb)
         bot.register_next_step_handler(message, process_message)
    except Exception:
        bot.send_message(message.chat.id, "При регистрации были введены некорректные данные, попробуйте еще раз")
        bot.send_message(message.chat.id, "Введите Ваш логин для входа")
        bot.register_next_step_handler(message, get_name)

def process_message(message):
    if message.text == "Справка":
        instruction(message.chat.id)
        bot.register_next_step_handler(message, process_message)
    elif message.text == "Информация о стране":
        facade.mode = "country"
        res = facade.country_rep.get_all_countries_names()
        keyb_i = keyb_new(res)
        bot.send_message(message.chat.id, "Выберите страну из списка", reply_markup=keyb_i)
        bot.register_next_step_handler(message, process_message)
    elif message.text == "Информация о климате":
        facade.mode = "climate"
        res = facade.country_rep.get_all_countries_names()
        keyb_i = keyb_new(res)
        bot.send_message(message.chat.id, "Выберите страну из списка", reply_markup=keyb_i)
        bot.register_next_step_handler(message, process_message)
    elif message.text == "Информация о городе":
        facade.mode = "city"
        res = facade.country_rep.get_all_countries_names()
        keyb_c = keyb_new(res)
        bot.send_message(message.chat.id, "Выберите страну из списка", reply_markup=keyb_c)
        bot.register_next_step_handler(message, process_message)
    elif message.text == "Выбрать отель":
        facade.mode = "hotel"
        res = facade.country_rep.get_all_countries_names()
        keyb_o = keyb_new(res)
        bot.send_message(message.chat.id, "Выберите страну из списка", reply_markup=keyb_o)
        bot.register_next_step_handler(message, process_message)
    elif message.text == "Изменить климат":
        facade.mode = "climate change"
        res = facade.country_rep.get_all_countries_names()
        keyb_o = keyb_new(res)
        bot.send_message(message.chat.id, "Выберите страну из списка", reply_markup=keyb_o)
    elif message.text == "Изменить отель":
        facade.mode = "hotel change"
        res = facade.country_rep.get_all_countries_names()
        keyb_o = keyb_new(res)
        bot.send_message(message.chat.id, "Выберите страну из списка", reply_markup=keyb_o)
    elif message.text == "Изменить номер":
        facade.mode = "room change"
        res = facade.country_rep.get_all_countries_names()
        keyb_o = keyb_new(res)
        bot.send_message(message.chat.id, "Выберите страну из списка", reply_markup=keyb_o)
    elif message.text == "Добавить отель":
        facade.mode = "hotel add"
        res = facade.country_rep.get_all_countries_names()
        keyb_o = keyb_new(res)
        bot.send_message(message.chat.id, "Выберите страну для которой хотите добавить отель", reply_markup=keyb_o)
    elif message.text == "Добавить номер":
        facade.mode = "room add"
        res = facade.country_rep.get_all_countries_names()
        keyb_o = keyb_new(res)
        bot.send_message(message.chat.id, "Выберите страну из списка", reply_markup=keyb_o)
    elif message.text == "Вывести пользователей":
        facade.mode = "users"
        try:
            res = facade.user_rep.get_all_users()
            for el in res:
                if el.permission == 0:
                    role = "администратор"
                elif el.permission == 1:
                    role = "модератор"
                else:
                    role = "пользователь"
                bot.send_message(message.chat.id, "ID: " + str(el.id) + ", логин:" + str(el.login) + ", права доступа: " + role)
        except:
            bot.send_message(message.chat.id, "Нет пользователей, возврат в главное меню\n")
        bot.register_next_step_handler(message, process_message)
    elif message.text == "Добавить пользователя":
        facade.mode = "user add"
        bot.send_message(message.chat.id, "Введите логин:")
        bot.register_next_step_handler(message, get_new_login)
    elif message.text == "Удалить  пользователя":
        facade.mode == "user delete"
        bot.send_message(message.chat.id, "Введите ID пользователя, которого хотите удалить:")
        bot.register_next_step_handler(message, delete_message)
    elif message.text == "Изменить пользователя":
        facade.mode == "user change"
        bot.send_message(message.chat.id, "Введите ID пользователя, которого хотите изменить:")
        bot.register_next_step_handler(message, user_id_message)
    elif message.text == "/stop" or message.text == "Выход":
        bot.send_message(message.chat.id, "Ждем Вас снова!", parse_mode='html',
                         reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, bot_start)
    else:
        try:
            if facade.mode == "room":
                int(message.text)
                kol = int(message.text)
                pr = facade.room.price * kol

                bot.send_message(message.chat.id, "Стоимость отдыха: " + str(pr))
                facade.menu_keyb()
                bot.send_message(message.chat.id, "Главное меню", reply_markup=facade.keyb)
                bot.register_next_step_handler(message, process_message)
            else:
                bot.send_message(message.chat.id, "Извините, я не понимаю")
                bot.register_next_step_handler(message, process_message)
        except ValueError:
            bot.send_message(message.chat.id, "Извините, я не понимаю")
            bot.register_next_step_handler(message, process_message)

def get_new_login(message):
    if len(message.text) <= 30:
        facade.user.set_login(message.text)
        elem = facade.user_rep.check_user_login(facade.user.login)
        if elem:
            bot.send_message(message.chat.id, "Этот логин недоступен")
            bot.send_message(message.chat.id, "Введите логин для входа")
            bot.register_next_step_handler(message, get_new_login)
        else:
            bot.send_message(message.chat.id, "Введите пароль")
            bot.register_next_step_handler(message, get_new_password)
    else:
        bot.send_message(message.chat.id, "Введен некорректный логин")
        bot.send_message(message.chat.id, "Введите логин для входа")
        bot.register_next_step_handler(message, get_new_login)

def get_new_password(message):
    if len(message.text) <= 20:
        facade.user.set_password(message.text)
        elem = facade.user_rep.check_user_password(facade.user.password)
        if elem:
            bot.send_message(message.chat.id, "Этот пароль недоступен")
            bot.send_message(message.chat.id, "Введите пароль для входа")
            bot.register_next_step_handler(message, get_new_password)
        else:
            bot.send_message(message.chat.id,
                             "Напишите какими правами доступа будет обладать данный аккаунт (Админимcтратор/Модератор/Пользователь)")
            bot.register_next_step_handler(message, add_perm)
    else:
        bot.send_message(message.chat.id, "Введен некорректный пароль")
        bot.send_message(message.chat.id, "Введите пароль для входа")
        bot.register_next_step_handler(message, get_new_password)

#add check
def delete_message(message):
    try:
        id = int(message.text)
        if abs(id - facade.id) != 0:
            facade.user_rep.delete_user(id)
            facade.menu_keyb()
            bot.send_message(message.chat.id, "Пользователь удален, возврат в главное меню", reply_markup=facade.keyb)
        else:
            facade.menu_keyb()
            bot.send_message(message.chat.id, "Пользователь не может быть удален (текущий аккаунт), возврат в главное меню", reply_markup=facade.keyb)
    except ValueError:
        facade.menu_keyb()
        bot.send_message(message.chat.id, "Введен неверный ID, возврат в главное меню", reply_markup=facade.keyb)
    bot.register_next_step_handler(message, process_message)

def user_id_message(message):
    try:
        facade.user.id = int(message.text)
        perm = facade.user_rep.get_user_perm(facade.user.id)

        if perm.permission == 0:
            bot.send_message(message.chat.id, "Данный пользователь не может быть изменен, так как он является администратором")
            bot.register_next_step_handler(message, process_message)
        elif abs(facade.user.id - facade.id) != 0:
            bot.send_message(message.chat.id, "Напишите какими правами доступа будет обладать данный аккаунт (Модератор/Пользователь)")
            bot.register_next_step_handler(message, user_perm_change_message)
        else:
            bot.send_message(message.chat.id, "Данный пользователь не может быть изменен (текущий аккаунт), возврат в главное меню\n")
            bot.register_next_step_handler(message, process_message)
    except Exception:
        facade.menu_keyb()
        bot.send_message(message.chat.id, "Введен неверный ID, возврат в главное меню", reply_markup=facade.keyb)
        bot.register_next_step_handler(message, process_message)

def user_perm_change_message(message):
    if message.text == 'Модератор' or message.text == 'модератор':
        perm = 1
    else:
        perm = 2
    facade.user_rep.update_user(facade.user.id, perm)
    bot.send_message(message.chat.id, "Пользователь изменен, возврат в главное меню")
    bot.register_next_step_handler(message, process_message)

#climate update
def month_message(message):
    if message.text in headlines.months:
        facade.climate.set_month(message.text)
        bot.send_message(message.chat.id,"Введите дневную температуру:")
        bot.register_next_step_handler(message, day_temp_message)
    else:
        facade.menu_keyb()
        bot.send_message(message.chat.id,"Введен неверный месяц, возврат в главное меню", reply_markup=facade.keyb)
        bot.register_next_step_handler(message, process_message)

def day_temp_message(message):
    try:
        day_temp = int(message.text)
        facade.climate.set_day_temp(day_temp)
        bot.send_message(message.chat.id,"Введите ночную температуру:")
        bot.register_next_step_handler(message, night_temp_message)
    except Exception:
        facade.menu_keyb()
        bot.send_message(message.chat.id,"Введена неверная дневная температура, возврат в главное меню", reply_markup=facade.keyb)
        bot.register_next_step_handler(message, process_message)

def night_temp_message(message):
    try:
        night_temp = int(message.text)
        facade.climate.set_night_temp(night_temp)
        bot.send_message(message.chat.id,"Введите температуру воды:")
        bot.register_next_step_handler(message, water_temp_message)
    except Exception:
        facade.menu_keyb()
        bot.send_message(message.chat.id,"Введена неверная ночная температура, возврат в главное меню", reply_markup=facade.keyb)
        bot.register_next_step_handler(message, process_message)

def water_temp_message(message):
    try:
        water_temp = int(message.text)
        facade.climate.set_water_temp(water_temp)
        facade.climate_rep.change_climtae_by_country(facade.climate.country, facade.climate.tur_month, facade.climate.day_temp,
                                              facade.climate.night_temp, facade.climate.water_temp)
        bot.send_message(message.chat.id, "Климат для страны " + facade.climate.country + " изменен\n")
        facade.menu_keyb()
        bot.send_message(message.chat.id,"Главное меню", reply_markup=facade.keyb)
        bot.register_next_step_handler(message, process_message)
    except Exception:
        facade.menu_keyb()
        bot.send_message(message.chat.id,"Введена неверная температура воды, возврат в главное меню", reply_markup=facade.keyb)
        bot.register_next_step_handler(message, process_message)

#add hotel
#hotel update
def hotel_name_message(message):
    if len(message.text) <= 60:
        el = facade.hotel_rep.check_hotel_name(facade.hotel.country, message.text)
        if el:
            facade.menu_keyb()
            bot.send_message(message.chat.id, "Данное название уже занято, возврат в главное меню",
                             reply_markup=facade.keyb)
            bot.register_next_step_handler(message, process_message)
        else:
            facade.hotel.name = message.text
            bot.send_message(message.chat.id, "Введите количество звезд от 1 до 5:")
            bot.register_next_step_handler(message, star_message)
    else:
        facade.menu_keyb()
        bot.send_message(message.chat.id, "Введена некорректное название, возврат в главное меню",
                         reply_markup=facade.keyb)
        bot.register_next_step_handler(message, process_message)

def star_message(message):
    try:
        stars = int(message.text)
        if stars < 1 or stars > 5:
            facade.menu_keyb()
            bot.send_message(message.chat.id, "Введена неверная звездность, возврат в главное меню", reply_markup=facade.keyb)
            bot.register_next_step_handler(message, process_message)
        else:
            facade.hotel.stars = stars
            facade.keyb = yes_no()
            bot.send_message(message.chat.id, "Выберите наличие пляжа", reply_markup=facade.keyb)
            bot.register_next_step_handler(message, beach_message)
    except Exception:
        facade.menu_keyb()
        bot.send_message(message.chat.id,"Введена неверная звездность, возврат в главное меню", reply_markup=facade.keyb)
        bot.register_next_step_handler(message, process_message)

def beach_message(message):
    if message.text == 'Да':
        facade.hotel.beach = True
        facade.keyb = yes_no()
        bot.send_message(message.chat.id, "Выберите наличие All Inclusive", reply_markup=facade.keyb)
        bot.register_next_step_handler(message, all_inc_message)
    elif message.text == 'Нет':
        facade.hotel.beach = False
        facade.keyb = yes_no()
        bot.send_message(message.chat.id, "Выберите наличие All Inclusive", reply_markup=facade.keyb)
        bot.register_next_step_handler(message, all_inc_message)
    else:
        facade.menu_keyb()
        bot.send_message(message.chat.id, "Неверный ввод, возврат в главное меню", reply_markup=facade.keyb)
        bot.register_next_step_handler(message, process_message)

def all_inc_message(message):
    if (message.text == 'Да') or (message.text == 'Нет'):
        if message.text == 'Да':
            facade.hotel.all_inc = True
        else:
            facade.hotel.all_inc = False
        if facade.mode == "hotel add":
            facade.hotel_rep.insert_hotel(facade.hotel.name, facade.hotel.stars, facade.hotel.beach, facade.hotel.all_inc, facade.hotel.country)
            bot.send_message(message.chat.id, "Отель для страны " + facade.hotel.country + " добвален\n")
        else:
           facade.hotel_rep.change_hotel_by_name(facade.hotel.id, facade.hotel.country, facade.hotel.name, facade.hotel.stars, facade.hotel.stars, facade.hotel.all_inc)
           bot.send_message(message.chat.id, "Отель для страны " + facade.hotel.country + " изменен\n")
        facade.menu_keyb()
        bot.send_message(message.chat.id, "Главное меню", reply_markup=facade.keyb)
    else:
        facade.menu_keyb()
        bot.send_message(message.chat.id, "Неверный ввод, возврат в главное меню", reply_markup=facade.keyb)
    bot.register_next_step_handler(message, process_message)

#room change
def room_name_message(message):
    if len(message.text) <= 45:
        #new
        el = facade.room_rep.check_room(facade.room.hotel, facade.room.name)
        if el:
            facade.menu_keyb()
            bot.send_message(message.chat.id, "Данное название уже занято, возврат в главное меню",
                             reply_markup=facade.keyb)
            bot.register_next_step_handler(message, process_message)
        else:
            facade.room.name = message.text
            bot.send_message(message.chat.id, "Введите вместимость")
            bot.register_next_step_handler(message, capacity_message)
    else:
        facade.menu_keyb()
        bot.send_message(message.chat.id, "Неверный ввод названия номера, возврат в главное меню", reply_markup=facade.keyb)
        bot.register_next_step_handler(message, process_message)

def capacity_message(message):
    try:
        if int(message.text) > 0:
            facade.room.capacity = int(message.text)
            bot.send_message(message.chat.id, "Введите этаж:")
            bot.register_next_step_handler(message, floor_message)
        else:
            facade.menu_keyb()
            bot.send_message(message.chat.id, "Неверный ввод, возврат в галвное меню", reply_markup=facade.keyb)
            bot.register_next_step_handler(message, process_message)
    except Exception:
        facade.menu_keyb()
        bot.send_message(message.chat.id,"Неверный ввод, возврат в галвное меню", reply_markup=facade.keyb)
        bot.register_next_step_handler(message, process_message)

def floor_message(message):
    try:
        if int(message.text) >= 0:
            facade.room.floor = int(message.text)
            bot.send_message(message.chat.id, "Введите цену:")
            bot.register_next_step_handler(message, price_message)
        else:
            facade.menu_keyb()
            bot.send_message(message.chat.id, "Неверный ввод, возврат в галвное меню", reply_markup=facade.keyb)
            bot.register_next_step_handler(message, process_message)
    except Exception:
        facade.menu_keyb()
        bot.send_message(message.chat.id,"Неверный ввод, возврат в главное меню", reply_markup=facade.keyb)
        bot.register_next_step_handler(message, process_message)


def price_message(message):
    try:
        facade.room.price = int(message.text)
        if facade.mode == "room add hotel":
            facade.room_rep.insert_room(facade.room.name, facade.room.capacity, facade.room.floor, facade.room.price, facade.room.hotel)
            bot.send_message(message.chat.id, "Номер для отеля " + facade.room.hotel + " добавлен\n")
        else:
           facade.room_rep.change_room(facade.room.id, facade.room.name, facade.room.capacity, facade.room.floor, facade.room.price)
           bot.send_message(message.chat.id, "Номер для отеля " + facade.room.hotel + " изменен\n")
        facade.menu_keyb()
        bot.send_message(message.chat.id, "Главное меню", reply_markup=facade.keyb)
    except Exception:
        facade.menu_keyb()
        bot.send_message(message.chat.id,"Неверный ввод, возврат в главное меню", reply_markup=facade.keyb)
    bot.register_next_step_handler(message, process_message)

@bot.callback_query_handler(func=lambda call:True)
def callback_react(call):
    if (facade.mode == "hotel"):
        #res = facade.hotel_rep.get_all_hotels_by_country(call.data)
        res = facade.get_all_hotels(call.data)
        keyb_h = hotel_keyb(res)
        facade.mode = "hotel in"
        bot.send_message(call.message.chat.id, call.data)
        bot.send_message(call.message.chat.id, "Выберите отель из списка", reply_markup=keyb_h)
    elif (facade.mode == "climate"):
        try:
           elem = facade.climate_rep.get_climate_by_country(call.data)
           bot.send_message(call.message.chat.id, call.data)
           bot.send_message(call.message.chat.id, "Самый подходящий для туризма месяц - " + elem.tur_month + ".\n" + "Температура днем: " +
                            str(elem.day_temp) + "\n" + "Температура ночью: " + str(elem.night_temp) + "\n" + "Температура воды:" + str(elem.water_temp))
        except:
            bot.send_message(call.message.chat.id, "Информация еще не занесена в базу\n")
    elif (facade.mode == "city"):
        try:
            res = facade.city_rep.get_all_cities(call.data)
            keyb_c = keyb_new(res)
            facade.mode = "city in"
            bot.send_message(call.message.chat.id, call.data)
            bot.send_message(call.message.chat.id, "Выберите город из списка", reply_markup=keyb_c)
        except:
            bot.send_message(call.message.chat.id, "Информация еще не занесена в базу\n")
    elif (facade.mode == "city in"):
        try:
            elem = facade.city_rep.get_city_by_name(call.data)
            bot.send_message(call.message.chat.id, "Имя города - " + elem.name + ".\n" + "Население: " +
                                  str(elem.population) + " миллионов.\n" + "Достопримечательность: " + elem.sight)
        except:
            bot.send_message(call.message.chat.id, "Информация еще не занесена в базу\n")
    elif (facade.mode == "hotel in"):
        try:
            elem = facade.hotel_rep.get_hotel_by_name(call.data)
            bot.send_message(call.message.chat.id, "Название отеля: " + elem.name + ".\n" + "Количество звезд:" + str(elem.stars) + ".\n")
            if elem.beach == True:
                bot.send_message(call.message.chat.id, "Пляж есть.\n")
            else:
                bot.send_message(call.message.chat.id, "Пляжа нет.\n")
            if elem.all_inc == True:
                bot.send_message(call.message.chat.id, "All inclusive есть.\n")
            else:
                bot.send_message(call.message.chat.id, "All inclusive нет.\n")
            facade.room.hotel = call.data
            res = facade.room_rep.get_all_rooms_by_hotel(elem.name)
            if res:
               facade.mode = "room"
               keyb_r = keyb_new(res)
               bot.send_message(call.message.chat.id, "Список номеров:\n", reply_markup=keyb_r)
        except:
            bot.send_message(call.message.chat.id, "Не могу найти соответствующую информацию в базе. Возможно, Вам стоит заново нажать на кнопку в главном меню.")
    elif (facade.mode == "room"):
        try:
            elem = facade.room_rep.get_room_by_name(call.data, facade.room.hotel)
            facade.room.price = elem.price
            bot.send_message(call.message.chat.id, "Название номера: " + elem.name + ".\n" + "Вместимость: " + str(elem.capacity) + "\n" + "Этаж: " + str(elem.floor) + "\n"
                             + "Цена в сутки:" + str(elem.price) + "\n")
            bot.send_message(call.message.chat.id, "Введите количество дней отдыха:")
        except:
            bot.send_message(call.message.chat.id, "Не могу найти соответствующую информацию в базе. Возможно, Вам стоит заново нажать на кнопку в главном меню.")
    elif (facade.mode == "country"):
        try:
            elem = facade.country_rep.get_country_by_name(call.data)
            bot.send_message(call.message.chat.id, "Столица - " + elem.capital + ".\n" + "Население: " +
                                           str(elem.population) + " миллионов.\n" + elem.descr +".")
            bot.send_photo(call.message.chat.id, open(elem.image, "rb"))
        except:
            bot.send_message(call.message.chat.id, "Не могу найти соответствующую информацию в базе. Возможно, Вам стоит заново нажать на кнопку в главном меню.")
    elif (facade.mode == "climate change"):
        facade.climate.set_country(call.data)
        keyb = keyboards.new_reply_keyb(headlines.months)
        bot.send_message(call.message.chat.id, "Выберите туристический месяц", reply_markup=keyb)
        bot.register_next_step_handler(call.message, month_message)
    elif (facade.mode == "hotel change"):
        res = facade.hotel_rep.get_all_hotels_by_country(call.data)
        if len(res) == 0:
            bot.send_message(call.message.chat.id, "В данном отеле пока нет номеров. Возврат в главное меню.")
            bot.register_next_step_handler(call.message, process_message)
        else:
            facade.hotel.country = call.data
            keyb_h = hotel_keyb(res)
            facade.mode = "hotel change in"
            bot.send_message(call.message.chat.id, call.data)
            bot.send_message(call.message.chat.id, "Выберите отель из списка", reply_markup=keyb_h)
    elif (facade.mode == "hotel change in"):
        facade.hotel.id = facade.hotel_rep.get_hotel_id_by_name(call.data)
        bot.send_message(call.message.chat.id, "Введите новое название отеля")
        bot.register_next_step_handler(call.message, hotel_name_message)
    elif (facade.mode == "hotel add"):
        facade.hotel.country = call.data
        bot.send_message(call.message.chat.id, "Введите название отеля")
        bot.register_next_step_handler(call.message, hotel_name_message)
    elif (facade.mode == "room change"):
        res = facade.hotel_rep.get_all_hotels_by_country(call.data)
        facade.hotel.country = call.data
        keyb_h = hotel_keyb(res)
        facade.mode = "room change hotel"
        bot.send_message(call.message.chat.id, call.data)
        bot.send_message(call.message.chat.id, "Выберите отель из списка", reply_markup=keyb_h)
    elif (facade.mode == "room change hotel"):
        res = facade.room_rep.get_all_rooms_by_hotel(call.data)
        if len(res) == 0:
            bot.send_message(call.message.chat.id, "В данном отеле пока нет номеров. Возврат в главное меню.")
            bot.register_next_step_handler(call.message, process_message)
        else:
            facade.room.hotel = call.data
            keyb_r = keyb_new(res)
            facade.mode = "room change in"
            bot.send_message(call.message.chat.id, call.data)
            bot.send_message(call.message.chat.id, "Выберите номер из списка", reply_markup=keyb_r)
    elif (facade.mode == "room change in"):
        facade.room.id = facade.room_rep.get_room_id(call.data, facade.room.hotel)
        bot.send_message(call.message.chat.id, "Введите новое название номера")
        bot.register_next_step_handler(call.message, room_name_message)
    elif (facade.mode == "room add"):
        res = facade.hotel_rep.get_all_hotels_by_country(call.data)
        facade.hotel.country = call.data
        keyb_h = hotel_keyb(res)
        facade.mode = "room add hotel"
        bot.send_message(call.message.chat.id, call.data)
        bot.send_message(call.message.chat.id, "Выберите отель из списка", reply_markup=keyb_h)
    elif (facade.mode == "room add hotel"):
        facade.room.hotel = call.data
        bot.send_message(call.message.chat.id, "Введите новое название номера")
        bot.register_next_step_handler(call.message, room_name_message)
    else:
        bot.send_message(call.message.chat.id, "Я не понимаю")


bot.polling(none_stop=True)
