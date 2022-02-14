import requests as req

class Bitrix():
    def __init__(self, url, user_id, data_order):
        self.result = self.sendMessage(url, user_id, data_order)

    def get_string_order(self, data):
        val = ''
        val2 = ''
        try:
            if data['position']:
                val2 = 'Нет нужного количества:\n'
                for v in range(len(data['position'])):
                    val2 = val2 + data['position'][v]['article'] + ' | ' + data['position'][v]['brand'] + ' | ' + str(data['position'][v]['not_order_count']) + '\n'
        except Exception:
            pass
        result = 'Поставщик {0} заказ № {1}\n{2}'.format(data['provider'], data['order'], val2)
        return result

    def sendMessage(self, url, user_id, data_order):
        string_order = self.get_string_order(data_order)
        data = {
            'DIALOG_ID': user_id,
            'MESSAGE': string_order,
            'SYSTEM': 'Y',
            'ATTACH': '',
            'URL_PREVIEW': 'Y',
            'KEYBOARD': '',
            'MENU': ''}
        bbb = req.post(url, data)
        return bbb.status_code




