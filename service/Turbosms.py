from selenium import webdriver
import time as t
# Указываем полный путь к geckodriver.exe на вашем ПК.
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Turbosms():
    def __init__(self, url, passwords, login, masiv, provider, api=False, balance=False, head=True):
        self.url = url
        self.passwords = passwords
        self.login = login
        self.head = head
        self.masiv = masiv
        self.caps = DesiredCapabilities().CHROME
        #self.caps["pageLoadStrategy"] = "normal"  # complete
        self.caps["pageLoadStrategy"] = "eager"  #  interactive
        # caps["pageLoadStrategy"] = "none"
        if head != True:
            self.options = webdriver.ChromeOptions()
            self.options.headless = True
            self.options.add_argument('--window-size=1024x800')
            self.options.add_argument('--ignore-certificate-errors-spki-list')
            self.driver = webdriver.Chrome('chromedriver.exe', chrome_options=self.options)
        else:
            self.driver = webdriver.Chrome('chromedriver.exe')
            self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.returnAnsver = {}
        self.returnAnsver['provider'] = provider
        self.logins()
        self.getBalance()

    def logins(self):
        t.sleep(1)
        self.driver.get(self.url)
        inBut = self.driver.find_element_by_xpath('//*[@id="login_btn"]')
        inBut.click()
        login = self.driver.find_element_by_id('auth_login')
        login.send_keys(self.login)
        passwords = self.driver.find_element_by_id('auth_password')
        passwords.send_keys(self.passwords)
        t.sleep(0.5)
        self.driver.find_element_by_id('submit_auth').click()

    def getBalance(self):
        t.sleep(1)
        balance_all = self.driver.find_element_by_xpath('//*[@id="main_navigation"]/div/ul[2]/li[2]/div[1]/div[2]')
        mess = 'Сервис: {0}\nБаланс : {1}'.format(self.returnAnsver['provider'], balance_all.text)
        self.returnAnsver['message'] = mess
        self.driver.close()
        self.driver.quit()


    def get_ansver(self):
        return self.returnAnsver