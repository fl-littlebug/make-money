import yaml
import time
import sys
from datetime import datetime
from selenium import webdriver

class add_to_cart:

    def __init__(self, conf_name):
        self.config = yaml.load(open('conf/{}.yaml'.format(conf_name), encoding='utf-8'), Loader=yaml.FullLoader)
        self.browser = webdriver.Chrome(executable_path=self.config['driver'])

    def login(self):
        element = self.find_element_by_class_name('sn-login')
        if element:
            element.click()
        time.sleep(self.config['login_time'])

    def run(self):
        self.browser.get(self.config['url'])
        while True:
            ok = self.find_element_by_class_name('sn-login')
            ok1 = self.find_by_text(self.config['buy_button'])
            ok2 = self.find_by_text(self.config['cart_button'])
            print(ok, ok1, ok2)
            if ok or not ok1 and not ok2:
                self.login()
            else:
                break
        self.op_click()
        try:
            seconds_delta = (self.config['op_time'] - datetime.now()).seconds
            if seconds_delta > 0:
                print('wait {}s'.format(seconds_delta))
                time.sleep(seconds_delta)
        except Exception as e:
            print(e)

        while not self.find_element_by_id('J_LinkBuy'):
            self.browser.refresh()

        print('start to next op')
        if self.config.get('is_cart', False):
            self.op_cart()
        if self.config.get('is_buy', False):
            while True:
                self.op_click()
                flag = self.op_buy()
                if flag:
                    break
                self.browser.refresh()
            for i in range(60):
                try:
                    self.browser.find_element_by_class_name('go-btn').click()
                except Exception as e:
                    print(e)
                    time.sleep(1)
                    continue

    def op_buy(self):
        try:
            element = self.browser.find_element_by_id('J_LinkBuy')
            self.click(element)
            return True
        except Exception as e:
            print(e)
            return False

    def op_cart(self):
        element = self.browser.find_element_by_id('J_LinkBasket')
        self.click(element)

    def op_click(self):
        if self.config.get('oper'):
            for oper in self.config['oper'].split(';'):
                element = self.find_by_link_text(oper)
                print(element)
                if not element:
                    continue
                self.click(element)

    def find_element_by_name(self, name):
        from selenium.common.exceptions import NoSuchElementException
        try:
            element = self.browser.find_element_by_name(name)
        except NoSuchElementException as e:
            print(e)
            return False
        else:
            return element

    def find_element_by_id(self, id):
        from selenium.common.exceptions import NoSuchElementException
        try:
            element = self.browser.find_element_by_id(id)
        except NoSuchElementException as e:
            print(e)
            return False
        else:
            return element

    def find_element_by_class_name(self, name):
        from selenium.common.exceptions import NoSuchElementException
        try:
            element = self.browser.find_element_by_class_name(name)
        except NoSuchElementException as e:
            print(e)
            return False
        else:
            return element

    def find_by_text(self, text):
        from selenium.common.exceptions import NoSuchElementException
        try:
            print("//*[contains(text(), '{}')]".format(text))
            element = self.browser.find_elements_by_xpath("//*[contains(text(), '{}')]".format(text))
        except NoSuchElementException as e:
            print(e)
            return False
        else:
            return element

    def find_by_link_text(self, text):
        from selenium.common.exceptions import NoSuchElementException
        try:
            element = self.browser.find_element_by_link_text(text)
        except NoSuchElementException as e:
            print(e)
            return False
        else:
            return element

    def click(self, element):
        # self.browser.execute_script("arguments[0].click();", element)
        from selenium.common.exceptions import ElementClickInterceptedException
        try:
            print('normal click')
            element.click()
        except ElementClickInterceptedException as e:
            print(e)
            self.browser.execute_script("arguments[0].click();", element)


if __name__ == '__main__':
    model = add_to_cart(sys.argv[1])
    model.run()
