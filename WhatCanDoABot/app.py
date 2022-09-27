import telebot
from telebot import types

from config import keys, TOKEN
from utils import ConvertionException, Converter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = 'Бот покажет некоторые возможности на что он способен. Узнать подробнее и заказать разработку бота ' \
           'можно у разработчика @DenisSamarkin'
           # 'можно у разработчика https://t.me/DenisSamarkin'

           # 'Чтобы узнать доступные валюты введите команду: /values \n'
    # bot.reply_to(message, text)
    bot.send_message(message.chat.id, 'Добро пожаловать!')
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)



@bot.message_handler(content_types=['text'])
def inline_key(a):
    if a.text == "1":
        mainmenu = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='Кнопка 1', callback_data='key1')
        key2 = types.InlineKeyboardButton(text='Кнопка 2', callback_data='key2')
        mainmenu.add(key1, key2)
        bot.send_message(a.chat.id, 'Это главное меню!', reply_markup=mainmenu)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "mainmenu":
        mainmenu = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='Кнопка 1', callback_data='key1')
        key2 = types.InlineKeyboardButton(text='Кнопка 2', callback_data='key2')
        mainmenu.add(key1, key2)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=mainmenu)
    elif call.data == "key1":
        next_menu = types.InlineKeyboardMarkup()
        key3 = types.InlineKeyboardButton(text='Кнопка 3', callback_data='key3')
        back = types.InlineKeyboardButton(text='Назад', callback_data='mainmenu')
        next_menu.add(key3, back)
        bot.edit_message_text('Это меню уровня 2, для кнопки1!', call.message.chat.id, call.message.message_id,
                              reply_markup=next_menu)
    elif call.data == "key2":
        next_menu2 = types.InlineKeyboardMarkup()
        key4 = types.InlineKeyboardButton(text='Кнопка 4', callback_data='key4')
        back = types.InlineKeyboardButton(text='Назад', callback_data='mainmenu')
        next_menu2.add(key4, back)
        bot.edit_message_text('Это меню уровня 2, для кнопки2!', call.message.chat.id, call.message.message_id,
                              reply_markup=next_menu2)



    # @bot.message_handler(content_types=['text', ])
    # def convert(message: telebot.types.Message):
    #     try:
    #         values = message.text.split(' ')
    #
    #         if len(values) != 3:
    #             raise ConvertionException('Слишком много параметров')
    #
    #         quote, base, amount = values
    #         total_base = Converter.convert(quote, base, amount)
    #     except ConvertionException as e:
    #         bot.reply_to(message, f'Ошибка пользователя\n{e}')
    #     except Exception as e:
    #         bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    #     else:
    #         text = f'Цена {amount} {quote} в {base} - {total_base}'
    #         bot.send_message(message.chat.id, text)


# try:
#     bot.poling(none_stop=True)
# except:
#     pass

bot.polling(none_stop=True)