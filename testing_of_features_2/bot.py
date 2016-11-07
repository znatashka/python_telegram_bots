import telebot
from telebot import types

from testing_of_features_2 import config

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['geophone'])
def geophone(message):
    # Эти параметры для клавиатуры необязательны, просто для удобства
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text='Отправить номер телефона', request_contact=True)
    button_geo = types.KeyboardButton(text='Отправить местоположения', request_location=True)
    keyboard.add(button_phone, button_geo)
    bot.send_message(
        message.chat.id,
        'Отправь мне свой номер телефона или поделись местоположением, жалкий человечишка!',
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: True)
def any_message(message):
    bot.reply_to(message, 'Сам {!s}'.format(message.text))


@bot.edited_message_handler(func=lambda message: True)
def edit_message(message):
    bot.edit_message_text(
        chat_id=message.chat.id,
        text='Сам {!s}'.format(message.text),
        message_id=message.message_id + 1
    )


if __name__ == '__main__':
    bot.polling(none_stop=True)
