import re
import traceback

import telebot
from telebot import types

from math_inline_bot import config

bot = telebot.TeleBot(config.token)
digits_pattern = re.compile(r'^[0-9]+ [0-9]+$', re.MULTILINE)


@bot.inline_handler(lambda query: len(query.query) is 0)
def empty_query(query):
    try:
        r = types.InlineQueryResultArticle(
            id='1', title='Бот "Математика"',
            description='Введите ровно 2 числа и получите результат!',
            input_message_content=types.InputTextMessageContent(
                parse_mode='Markdown',
                message_text='Эх, зря я не ввёл 2 числа :('
            )
        )
        bot.answer_inline_query(query.id, [r])
    except Exception as e:
        traceback.print_exception(type(e), e, None)


@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    try:
        matches = re.match(digits_pattern, query.query)
    except AttributeError:
        return

    num1, num2 = matches.group().split()
    try:
        m_sum = int(num1) + int(num2)
        r_sum = types.InlineQueryResultArticle(
            id='1', title='Сумма',
            # Описание отображается в подсказке,
            # input_message_content - то, что будет отправлено в виде сообщения
            description='Результат: {!s}'.format(m_sum),
            input_message_content=types.InputTextMessageContent(
                message_text='{!s} + {!s} = {!s}'.format(num1, num2, m_sum)
            ),
            thumb_url=config.plus_icon,
            thumb_width=48, thumb_height=48
        )
        m_sub = int(num1) - int(num2)
        r_sub = types.InlineQueryResultArticle(
            id='2', title='Разность',
            description='Результат: {!s}'.format(m_sub),
            input_message_content=types.InputTextMessageContent(
                message_text='{!s} - {!s} = {!s}'
            ),
            thumb_url=config.minus_icon,
            thumb_width=48, thumb_height=48
        )
        # Учтем деление на ноль и подготовим 2 варианта развития событий
        if num2 is not '0':
            m_div = int(num1) / int(num2)
            r_div = types.InlineQueryResultArticle(
                id='3', title='Частное',
                description='Результат: {0:.2f}'.format(m_div),
                input_message_content=types.InputTextMessageContent(
                    message_text='{0!s} / {1!s} = {2:.2f}'.format(num1, num2, m_div)
                ),
                thumb_url=config.divide_icon,
                thumb_width=48, thumb_height=48
            )
        else:
            r_div = types.InlineQueryResultArticle(
                id='3', title='Частное',
                description='На ноль делить нельзя!',
                input_message_content=types.InputTextMessageContent(
                    message_text='Я нехороший чеорвек и делю на ноль!',
                    disable_web_page_preview=True
                ),
                thumb_url=config.error_icon,
                thumb_width=48, thumb_height=48,
                # Сделаем превью кликабельным, по нажатию юзера направят по ссылке
                url='https://ru.wikipedia.org/wiki/'
                    '%D0%94%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5_%D0%BD%D0%B0_%D0%BD%D0%BE%D0%BB%D1%8C',
                # Не будем показывать URL в подсказке
                hide_url=True
            )
        m_mul = int(num1) * int(num2)
        r_mul = types.InlineQueryResultArticle(
            id='4', title='Произведение',
            description='Результат: {!s}'.format(m_mul),
            input_message_content=types.InputTextMessageContent(
                message_text='{!s} * {!s} = {!s}'.format(num1, num2, m_mul)
            ),
            thumb_url=config.multiply_icon,
            thumb_width=48, thumb_height=48
        )
        # В нашем случае, результаты вычислений не изменятся даже через долгие годы, НО!
        # если где-то допущена ошибка и cache_time уже выставлен большим, то это уже никак не исправить (наверное)
        # Для справки: 2147483646 секунд - это 68 с копейками лет :)
        bot.answer_inline_query(query.id, [r_sum, r_sub, r_div, r_mul], cache_time=2147483646)
    except Exception as e:
        traceback.print_exception(type(e), e, None)


if __name__ == '__main__':
    bot.polling(none_stop=True)
