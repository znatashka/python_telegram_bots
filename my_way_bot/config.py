from emoji import emojize

TOKEN = '271501134:AAHUYvRmTX1bP6KqeaA18IzyS96Hv5UTyaE'

# URL templates
MY_WAY_URL_TEMPLATE = 'http://myway.io/myway/?q='
SEARCH_ADDRESS_URL_TEMPLATE = 'http://search.maps.sputnik.ru/search/addr?q='

# Emoji
IN_METRO = emojize(':metro:')
IN_CITY = emojize(':pedestrian:')
FINISH = emojize(':chequered_flag:')
I_SIDE = emojize(':heavy_exclamation_mark_symbol:')

# Error messages
WAY_NOT_FOUND = 'Маршрут не найден! {!s}'.format(emojize(':pensive_face:'))
ADDRESS_NOT_FOUND = 'Адрес не найден! {!s}'.format(emojize(':pensive_face:'))
