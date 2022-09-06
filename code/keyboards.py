import telebot
from telebot import types
from abc import ABCMeta, abstractmethod

class Menu():
    __metaclass__ = ABCMeta

class UserMenu(Menu):
    def __init__(self):
        keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Информация о стране")
        item2 = types.KeyboardButton("Информация о климате")
        item5 = types.KeyboardButton("Информация о городе")
        item4 = types.KeyboardButton("Выбрать отель")
        item3 = types.KeyboardButton("Справка")
        item6 = types.KeyboardButton("Выход")
        keyb.add(item1, item2, item5, item4, item3, item6)
        self.keyb = keyb

class ModerMenu(Menu):
    def __init__(self):
        keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Информация о стране")
        item2 = types.KeyboardButton("Информация о климате")
        item5 = types.KeyboardButton("Информация о городе")
        item4 = types.KeyboardButton("Выбрать отель")
        item3 = types.KeyboardButton("Справка")
        item6 = types.KeyboardButton("Изменить климат")
        item7 = types.KeyboardButton("Изменить отель")
        item8 = types.KeyboardButton("Изменить номер")
        item9 = types.KeyboardButton("Добавить отель")
        item10 = types.KeyboardButton("Добавить номер")
        item11 = types.KeyboardButton("Выход")
        keyb.add(item1, item2, item5, item4, item3, item6, item7, item8, item9, item10, item11)
        self.keyb = keyb

class AdminMenu(Menu):
    def __init__(self):
        keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Информация о стране")
        item2 = types.KeyboardButton("Информация о климате")
        item5 = types.KeyboardButton("Информация о городе")
        item4 = types.KeyboardButton("Выбрать отель")
        item3 = types.KeyboardButton("Справка")
        item6 = types.KeyboardButton("Изменить климат")
        item7 = types.KeyboardButton("Изменить отель")
        item8 = types.KeyboardButton("Изменить номер")
        item9 = types.KeyboardButton("Добавить отель")
        item10 = types.KeyboardButton("Добавить номер")
        item11 = types.KeyboardButton("Вывести пользователей")
        item12 = types.KeyboardButton("Добавить пользователя")
        item13 = types.KeyboardButton("Удалить  пользователя")
        item14 = types.KeyboardButton("Изменить пользователя")
        item15 = types.KeyboardButton("Выход")
        keyb.add(item1, item2, item5, item4, item3, item6, item7, item8, item9, item10, item11, item12, item13, item14, item15)
        self.keyb = keyb


def new_reply_keyb(data):
    keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for el in data:
        item = types.KeyboardButton(el)
        keyb.add(item)
    return keyb

# def menu_user():
#     keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     item1 = types.KeyboardButton("Информация о стране")
#     item2 = types.KeyboardButton("Информация о климате")
#     item5 = types.KeyboardButton("Информация о крупнейшем городе")
#     item4 = types.KeyboardButton("Выбрать отель")
#     item3 = types.KeyboardButton("Справка")
#     keyb.add(item1, item2, item5, item4, item3)
#     return keyb
#
# def menu_moder():
#     keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     item1 = types.KeyboardButton("Информация о стране")
#     item2 = types.KeyboardButton("Информация о климате")
#     item5 = types.KeyboardButton("Информация о городе")
#     item4 = types.KeyboardButton("Выбрать отель")
#     item3 = types.KeyboardButton("Справка")
#     item6 = types.KeyboardButton("Изменить страну")
#     item7 = types.KeyboardButton("Изменить климат")
#     item8 = types.KeyboardButton("Изменить город")
#     item9 = types.KeyboardButton("Изменить отель")
#     item10 = types.KeyboardButton("Изменить комнату")
#     keyb.add(item1, item2, item5, item4, item3, item6, item7, item8, item9, item10)
#     return keyb
#
# def menu_keyb(permission):
#     if permission == 2:
#         keyb = menu_user()
#     elif permission == 1:
#         keyb = menu_moder()
#     #admin
#     return keyb


