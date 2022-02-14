######SQLite#######
NAME_FILE_DB = "db\provider.db"

#######connect DB########
HOST = '127.0.0.1'
PORT = 3306
DB = 'provider'
USER_local = ''
PASS_local = ''
USER = ''
PASS = ''

#######SSH#################
HOST_SSH = ''
PORT_SSH = ''
USER_SSH = ''
PASS_SSH = ''

#######telegram##########
TOKEN = ''
TOKENMESSAGE = ''
NAME = 'JARVIS'
URL_SEND = 'https://api.telegram.org/bot'

#######Status_kod###########
STATUS_KOD = {
    '100': 'NEW',
    '200': 'OK',
    '201': 'Нет достаточного количества',
    '300': 'Нет на складе Житомир, есть на других складах',
    '400': 'Не удалось создать заказ',
    '401': 'Отказ заказа с другого склада',
    '402': 'Нет такого артикула/бренда',
    '403': 'Отсутствует',
    '405': 'Не удалось добавить позицию в заказ',
    '406': 'Не удалось добавить позицию в заказ, неизвестная ошибка',
    '407': 'Логическая ошибка с количеством'
}

reply_markup = {
    'inline_keyboard': [[{'text': 'Заказать', 'callback_data': 'order'}, {'text': 'Не заказывать', 'callback_data': 'not_order'}]]}
