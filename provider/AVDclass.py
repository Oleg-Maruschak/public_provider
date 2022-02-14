from selenium import webdriver
import time as t
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import function as f
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import configs


class AVD():
    def __init__(self, url, passwords, login, cookie, masiv, provider, api, numberOrder=False, balance=False, head=True):
        self.url = url
        self.passwords = passwords
        self.login = login
        self.cookie = cookie
        self.head = head
        self.numberOrder = numberOrder
        self.api = api
        self.masiv = masiv
        self.options = webdriver.ChromeOptions()
        self.caps = DesiredCapabilities().CHROME
        self.caps["pageLoadStrategy"] = "none"
        if head != True:
            self.options.add_argument('headless')
            self.options.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=self.caps, chrome_options=self.options)
        else:
            self.options.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=self.caps, chrome_options=self.options)
        self.driver.implicitly_wait(5)
        self.returnAnsver = {}
        self.returnAnsver['provider'] = provider
        self.returnAnsver['ansver'] = False
        self.returnAnsver['position'] = []
        if balance == True:
            self.getBalance()
        else:
            self.search()


    def get_ansver(self):
        return self.returnAnsver


    def logins(self):
        #self.driver.get(self.url)
        login = self.driver.find_element_by_id('loginform-login')
        login.send_keys(self.login)
        passwords = self.driver.find_element_by_id('loginform-password')
        passwords.send_keys(self.passwords)
        self.driver.find_element_by_name('login-button').click()


    def newOrder(self, login, i=0):
        if login:
            self.driver.find_element_by_xpath('//a[@class="basket_button_header history_open_orders_button"]').click()
        try:
            self.driver.find_element_by_xpath('//button[@class="btn btn-default catalog_search_btn createNewOrder add-order-btn-margin"]').click()
        except Exception:
            try:
                self.driver.find_element_by_xpath('//button[@class="btn btn-default catalog_search_btn add-order-btn createNewOrder"]').click()
            except exceptions.ElementClickInterceptedException:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                wait = WebDriverWait(self.driver, 5)
                alert = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'error-window')))
                if alert.text == 'Произошла ошибка, повторите запрос позже.':
                    self.driver.refresh()
                    self.newOrder(login, i + 1)
                    if i >= 5:
                        return False
            except Exception:
                self.driver.refresh()
                self.newOrder(login, i + 1)
                if i >= 5:
                    return False


    def refactor_cookie(self, cookies):
        cook = []
        for i in cookies:
            if i['name'] == 'session_id' or i['name'] == '_csrf':
                cook.append({'name': i['name'], 'value': i['value']})
        return cook


    def set_list_articles_in_bd(self):
        for value in self.masiv:
            f.set_in_order(self.api, self.returnAnsver['order'], value['article'], value['brand'], value['count'], self.returnAnsver['provider'], 100, configs.STATUS_KOD['100'])


    def search(self):
        login = False
        ###########
        self.driver.get(self.url)
        try:
            #self.driver.get(self.url)
            t.sleep(0.5)
            for i in eval(self.cookie):
                self.driver.add_cookie(i)
            self.driver.get('https://shop.avdtrade.com.ua/basket')
            self.driver.find_element_by_id('button-min-menu')
        except Exception:
            self.logins()
            login = True
            cook = self.refactor_cookie(self.driver.get_cookies())
            f.set_cookie(self.api, self.returnAnsver['provider'], cook)
        ############
        if self.numberOrder == False or self.numberOrder == None:
            i = 0
            while True:
                self.newOrder(login)
                t.sleep(3)
                i = i + 1
                numberOrders = self.driver.find_element_by_id('TitleHederNumber').text
                self.returnAnsver['order'] = numberOrders.replace('> ', '')
                if numberOrders != '':
                    break
                elif i == 5:
                    self.returnAnsver['message'] = configs.STATUS_KOD['400']
                    self.returnAnsver['status_kod'] = 400
                    self.driver.close()
                    self.driver.quit()
                    break
        else:
            self.returnAnsver['order'] = self.numberOrder
        self.set_list_articles_in_bd()
        self.driver.get('https://shop.avdtrade.com.ua/catalog')
        for value in self.masiv:
            self.zakaz(value['article'], value['brand'], value['count'], value['order'])
        self.driver.close()
        self.driver.quit()


    def search_article(self, article, brands):
        art = self.driver.find_element_by_id('js-text-article')
        art.clear()
        art.send_keys(article)
        self.driver.find_element_by_id('js-check-brand').click()
        self.driver.find_element_by_xpath('//span[@id="select2-js-text-brand-container"]').click()
        brand = self.driver.find_element_by_class_name('select2-search__field')
        brand.clear()
        brand.send_keys(brands)
        self.driver.implicitly_wait(0.5)
        if self.driver.find_element_by_xpath('//ul[@id="select2-js-text-brand-results"]').text == 'Нет совпадений':
            return False
        else:
            brand.send_keys(Keys.RETURN)
            try:
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.invisibility_of_element((By.ID, 'loader')))
            finally:
                pass
            t.sleep(2)
            return True


    def set_count(self, counts, article, brands, order):
        count = self.getCountArticle()
        if count:
            self.inOrders(article, brands, counts, order)
        elif int(count) == 0:
            f.update_in_order_err(self.api, self.returnAnsver['order'], article, brands, 0, configs.STATUS_KOD['403'], 403)
        elif int(count) > int(counts):
            self.inOrders(article, brands, count, order)
        else:
            if int(count) < int(counts):
                f.update_in_order_err(self.api, self.returnAnsver['order'], article, brands, int(counts)-int(count), configs.STATUS_KOD['201'], 201)
                self.inOrders(article, brands, count, order)
            else:
                f.update_in_order_err(self.api, self.returnAnsver['order'], article, brands, 0, configs.STATUS_KOD['407'], 407)


    def get_orders(self, order):
        if order == '':
             return_order = self.driver.find_element_by_xpath('//*[@id="js-result-search"]/div/div/div[1]/div[4]/div/div/strong').text
             if return_order == 'На складе':
                 return True
             else:
                 return False
        else:
            return True


    def zakaz(self, article, brands, counts, order):
        #t.sleep(5)
        if self.search_article(article, brands) != True:
            f.update_in_order_err(self.api, self.returnAnsver['order'], article, brands, 0, configs.STATUS_KOD['402'], 402)
        else:
            try:
                self.driver.find_element_by_xpath('//*[@id="js-result-search"]/strong')
                article_new = article.replace('.', '').replace(' ', '').replace('-', '')
                self.search_article(article_new, brands)
                self.set_count(counts, article, brands, order)
            except Exception:
                self.set_count(counts, article, brands, order)


    def getCountArticle(self):
        self.driver.implicitly_wait(5)
        countArticle = self.driver.find_element_by_xpath('//*[@id="js-result-search"]/div/div/div[1]/div[5]/div/div/strong')
        if countArticle.text[0] == '>':
            return True
        else:
            return countArticle.text


    def inOrders(self, article, brands, countArt, order):
        newOrder = True
        if self.numberOrder != False and self.numberOrder != None:
            order = self.returnAnsver['order']
        if self.get_orders(order):
            if countArt != 1:
                count = self.driver.find_element_by_name('amount')
                count.send_keys(Keys.BACKSPACE)
                count.send_keys(countArt)
            try:
                but = self.driver.find_element_by_xpath('//*[@id="js-result-search"]/div/div/div[1]/div[7]/div/div/div/button')
                but.send_keys(Keys.RETURN)
                t.sleep(2)
                try:
                    self.driver.implicitly_wait(3)
                    modelWindow = self.driver.find_element_by_id('buyModal')
                    list = modelWindow.find_elements_by_class_name('panel-body')
                    for i in list:
                        listColumn = i.find_elements_by_class_name('table_centered')
                        numberOrder = listColumn[3].text
                        if numberOrder == self.returnAnsver['order']:
                            listColumn[0].click()
                            newOrder = False
                    if newOrder:
                        self.driver.find_element_by_xpath('//*[@id="buyModal"]/div/div/div[3]/div/button[1]').click()
                except Exception:
                    pass
                try:
                    self.driver.implicitly_wait(2)
                    self.driver.find_element_by_xpath('//*[@id="error_message"]/p')
                    f.update_in_order_err(self.api, self.returnAnsver['order'], article, brands, 0, configs.STATUS_KOD['406'], 406)
                except Exception:
                    pass
                f.update_in_order(self.api, self.returnAnsver['order'], article, brands, configs.STATUS_KOD['200'], 200, int(countArt))
            except Exception:
                f.update_in_order_err(self.api, self.returnAnsver['order'], article, brands, 0, configs.STATUS_KOD['405'], 405)
        else:
            f.update_in_order_err(self.api, self.returnAnsver['order'], article, brands, 0, configs.STATUS_KOD['300'], 300)
            self.returnAnsver['ansver'] = True ##### Убрать, заменить проверку вместо Истины использовать статус код 300


    def getBalance(self):
        t.sleep(8)
        listInfo = []
        listInfo.append(self.returnAnsver['provider'])
        self.driver.get('https://shop.avdtrade.com.ua/cabinet')
        balance_all = "Общая задолженность: {0}".format(self.driver.find_element_by_xpath('//*[@id="page_order_shipping"]/div/div/div[1]/div[1]/p[1]/span').text)
        listInfo.append(balance_all)
        try:
            stop = self.driver.find_element_by_id('js-get-debit-credit').text
            listInfo.append(stop)
        except Exception:
            pass
        try:
            debt_balance = "Просроченная задолженность: {0}".format(self.driver.find_element_by_xpath('//*[@id="debts_top"]').text)
            listInfo.append(debt_balance)
        except Exception:
            pass
        mess = ''
        for val in listInfo:
            mess = mess + "{0}\n".format(val)
        self.returnAnsver['message'] = mess
        self.driver.close()
        self.driver.quit()