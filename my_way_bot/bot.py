import logging

import eventlet
import requests
import telebot
from telebot import types

from my_way_bot.config import *

bot = telebot.TeleBot(TOKEN)


def get_data(url_template, params):
    timeout = eventlet.Timeout(10)
    try:
        way = requests.get(url_template + params)
        return way.json()
    except eventlet.timeout.Timeout:
        logging.warning('Got Timeout while retrieving MY WAY JSON data. Cancelling...')
        return None
    finally:
        timeout.cancel()


def parse_way(way_json):
    result_ = way_json['result'][0]
    station_ = result_['exit']['station']

    station_name_ = station_['name']
    line_name_ = station_['line']['name']
    distance_ = result_['distance']

    indoor_instructions_ = result_['indoor']['instructions']
    side_ = result_['indoor']['side']

    exit_instructions_ = []
    for instr in result_['instructions']:
        exit_instructions_.append(instr['text'])

    indoor_instructions_[0] = '<i>{!s}</i>'.format(indoor_instructions_[0])
    exit_instructions_[0] = '<i>{!s}</i>'.format(exit_instructions_[0])

    return {
        'station_name': station_name_,
        'line_name': line_name_,
        'distance': distance_,
        'side': side_,
        'in_metro': ' &#8594; '.join(indoor_instructions_),
        'outside': ' &#8594; '.join(exit_instructions_)
    }


def create_message(address, way):
    return '<b>{address}</b>\n{metro} <b>{station_name}</b> (<i>{line_name}</i>) [<i>{distance}</i>м]\n{i_side}{side}\n{in_metro}\n{city} {outside} {finish}'.format(
        address=address,
        station_name=way['station_name'],
        line_name=way['line_name'],
        distance=way['distance'],
        side=way['side'],
        metro=IN_METRO,
        in_metro=way['in_metro'],
        city=IN_CITY,
        outside=way['outside'],
        finish=FINISH,
        i_side=I_SIDE
    )


def send_way(chat_id, way):
    logging.debug(way)
    bot.send_message(chat_id, way, parse_mode='HTML')


def send_error(chat_id, message):
    bot.send_message(chat_id, message)


def check_address(address_json):
    address_json = get_data(SEARCH_ADDRESS_URL_TEMPLATE, address_json)
    if len(address_json['result']) > 1:
        features_ = address_json['result']['address'][0]['features']
        if len(features_) == 1 or bool(features_[0]['properties']['full_match']):
            return features_[0]['properties']['display_name']
    else:
        return None


@bot.message_handler(func=lambda message: True, content_types=['text'])
def my_way(message):
    address = check_address(message.text)
    if address:
        way_json = get_data(MY_WAY_URL_TEMPLATE, address)
        if way_json is None:
            send_error(message.chat.id, WAY_NOT_FOUND)
        else:
            way = parse_way(way_json)
            send_way(message.chat.id, create_message(address, way))
    else:
        send_error(message.chat.id, ADDRESS_NOT_FOUND)


def send_way_inline(query_id, way):
    logging.debug(way)
    answer = types.InlineQueryResultArticle(
        id='1', title='Поиск маршрута',
        description='Маршрут найден! {!s}'.format(emojize(':smiling_face_with_smiling_eyes:')),
        input_message_content=types.InputTextMessageContent(
            message_text=way,
            parse_mode='HTML'
        )
    )
    bot.answer_inline_query(query_id, [answer])


def send_error_inline(query_id, message):
    answer = types.InlineQueryResultArticle(
        id='1', title='Маршрут',
        description=message,
        input_message_content=types.InputTextMessageContent(
            message_text=message
        )
    )
    bot.answer_inline_query(query_id, [answer])


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def my_way_inline(query):
    address = check_address(query.query)
    if address:
        way_json = get_data(MY_WAY_URL_TEMPLATE, address)
        if way_json is None:
            send_error_inline(query.id, WAY_NOT_FOUND)
        else:
            way = parse_way(way_json)
            send_way_inline(query.id, create_message(address, way))
    else:
        send_error_inline(query.id, ADDRESS_NOT_FOUND)


def set_up_logger():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s')
    root_logger.addHandler(handler)


if __name__ == '__main__':
    set_up_logger()
    bot.polling(none_stop=True)
