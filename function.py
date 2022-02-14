import requests as req
import configs
import json
from model import Connect_db
def testSend(user_id, data):
    value = {
        'chat_id': user_id,
        'text': data
    }
    send = req.post(configs.URL_SEND + configs.TOKEN + '/sendMessage', value)

def send_message_telegram(user_id, data):
    get_mes = return_message(data)
    value = {
        'chat_id': user_id,
        'text': get_mes
    }
    if data['ansver']:
        try:
            value['reply_markup'] = json.dumps(configs.reply_markup)
        except Exception:
            pass
    req.post(configs.URL_SEND+configs.TOKEN+'/sendMessage', value)


def return_message(data):
    val = ''
    val2 = ''
    try:
        if data['position']:
            val2 = 'Нет нужного количества:\n'
            for v in range(len(data['position'])):
                val2 = val2 + data['position'][v]['article'] + ' | ' + data['position'][v]['brand'] + ' | ' + str(
                    data['position'][v]['not_order_count']) + '\n'
    except Exception:
        pass
    result = 'Поставщик {0} заказ № {1}\n{2}'.format(data['provider'], data['order'], val2)
    return result


def set_in_order(api, order, article, brands, countArt, provider, status_kod, message):
    db = Connect_db()
    db.set_inOrder(api, order, article, brands, countArt, provider, status_kod, message)
    db.closes()


def set_cookie(api, provider, cookie):
    db = Connect_db()
    db.set_cookies(api, provider, cookie)
    db.closes()


def update_in_order_err(api, order, article, brand, count_fact, message, status_kod):
    db = Connect_db()
    db.update_in_order_err(api, order, article, brand, count_fact, message, status_kod)
    db.closes()


def update_in_order(api, order, article, brand, message, status_kod, count_fact):
    db = Connect_db()
    db.update_in_order(api, order, article, brand, message, status_kod, count_fact)
    db.closes()


def get_result_order(api, order, provider):
    name_column = ('api', 'order', 'provider', 'article', 'brand', 'counts', 'count_fact', 'in', 'send_question', 'go', 'status_kod', 'message', 'date')
    value_order = {}
    db = Connect_db()
    rows_value = db.get_result_order(api, order, provider)
    if len(rows_value) > 0:
        value_order['provider'] = rows_value[0][2]
        value_order['order'] = rows_value[0][1]
        value_order['position'] = []
        for i in rows_value:
            dic = {}
            for n, e in enumerate(i):
                if n > 2:
                    dic[name_column[n]] = i[n]
            value_order['position'].append(dic)
    else:
        value_order = False
    db.closes()
    return value_order

