import pymysql
import sqlite3 as sql
import configs
from datetime import datetime
from sshtunnel import SSHTunnelForwarder


class Connect_db():
    def __init__(self, api=False):
        self.api = api
        self.con = sql.connect(configs.NAME_FILE_DB)
        self.date = datetime.now()

        #self.server = SSHTunnelForwarder(
        #            (configs.HOST_SSH, configs.PORT_SSH),
        #            ssh_password=configs.PASS_SSH,
        #            ssh_username=configs.USER_SSH,
        #            remote_bind_address=(configs.HOST, configs.PORT))
        #self.server.start()
        #self.con = pymysql.connect(host=configs.HOST, port=self.server.local_bind_port, user=configs.USER, password=configs.PASS, db=configs.DB, cursorclass=pymysql.cursors.DictCursor)


    def select_api(self):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM `api_key` WHERE `key_value` = '%s'" % self.api)
        #rows = cur.fetchone()
        rows = list(cur.fetchone())
        cur.close()
        if rows == None:
            value = 'API не существует!!!'
            return value
        #elif rows['off'] == 0:
        elif rows[4] == 0:
            value = 'Доступ ключу {0} закрыт'.format(self.api)
            return value
        else:
            return True


    def select_url(self, cod):
        list_value = {}
        cur = self.con.cursor()
        cur.execute("SELECT * FROM `provider` WHERE `cod_provider` = '%s'" % cod)
        #rows = cur.fetchone()
        rows = list(cur.fetchone())
        cur.close()
        if rows == None:
            list_value['err'] = 'Не верно указан поставщик %s !' % (cod)
            return list_value
        else:
            #return rows['url']
            list_value['url'] = rows[4]
            list_value['login'] = rows[5]
            list_value['pass'] = rows[6]
            list_value['cookie'] = rows[7]
            return list_value


    def select_message(self):
        value = {}
        cur = self.con.cursor()
        cur.execute("SELECT * FROM `send_message` WHERE `key_value` = '%s' AND `off` = '1'" % self.api)
        #rows = cur.fetchone()
        rows = list(cur.fetchone())
        cur.close()
        if rows != None:
            value['url'] = rows[4]
            #value['url'] = rows['url_bitrix']
            bit = rows[3].split(',')
            #bit = rows['bitrix'].split(',')
            value['bitrix'] = bit
            tel = rows[2].split(',')
            #tel = rows['telegram'].split(',')
            value['telegram'] = tel
            value['off'] = rows[5]
            #value['off'] = rows['off']
        return value


    def set_api_message(self, new_list):
        cur = self.con.cursor()
        cur.execute("UPDATE `send_message` SET `telegram`= '%s' WHERE `key_value` = '%s'" % (new_list, self.api))
        cur.close()
        self.con.commit()


    def set_inOrder(self, api, order, article, brand, count_art, provider, status_kod, message):
        cur = self.con.cursor()
        cur.execute(
            "INSERT INTO `in_order`('api', 'order', 'article', 'brand', 'counts', 'provider', 'status_kod', 'message', 'date') VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
            % (api, order, article, brand, count_art, provider, status_kod, message, self.date.strftime('%Y-%m-%d %H:%M:%S'))
        )
        cur.close()


    def set_cookies(self, api, provider, cookie):
        cur = self.con.cursor()
        cur.execute(f'UPDATE `provider` SET `cookie` = "{cookie}" WHERE `key_value` = "{api}" and `cod_provider` = "{provider}"')
        # if update_row.rowcount == 0:
        #     cur.execute(f'INSERT INTO `provider` (`api`, `provider`, `cookie`)  VALUES ("{api}", "{provider}", "{cookie}")')
        cur.close()


    def update_in_order_err(self, api, order, article, brand, count_fact, message, status_kod):
        cur = self.con.cursor()
        cur.execute(
            f"UPDATE `in_order` SET `message` = '{message}', `status_kod` = '{status_kod}', `count_fact` = '{count_fact}', `date` = '{self.date.strftime('%Y-%m-%d %H:%M:%S')}' WHERE `api` = '{api}' AND `order` = '{order}' AND `article` = '{article}' AND `brand` = '{brand}'"
        )
        cur.close()


    def update_in_order(self, api, order, article, brand, message, status_kod, count_fact):
        cur = self.con.cursor()
        cur.execute(
            f"UPDATE `in_order` SET `in` = 1, `message` = '{message}', `status_kod` = '{status_kod}', `count_fact` = '{count_fact}', `date` = '{self.date.strftime('%Y-%m-%d %H:%M:%S')}' WHERE `api` = '{api}' AND `order` = '{order}' AND `article` = '{article}' AND `brand` = '{brand}'"
        )
        cur.close()


    def get_result_order(self, api, order, provider):
        cur = self.con.cursor()
        value = cur.execute(f"SELECT * FROM `in_order` WHERE `api` = '{api}' AND `order` = '{order}' AND `provider` = '{provider}'")
        rows_value = value.fetchall()
        cur.close()
        return rows_value


    def closes(self):
        self.con.commit()
        self.con.cursor().close()
        self.con.close()
        #self.server.stop()



