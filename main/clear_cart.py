# -*- coding: <encoding name> -*- : # -*- coding: utf-8 -*-
import yaml
import time
import sys
from datetime import datetime
from selenium import webdriver

class clear_cart:

    def __init__(self, conf_name):
        self.config = yaml.load(open('conf/{}.yaml'.format(conf_name), encoding='utf-8'), Loader=yaml.FullLoader)
        self.browser = webdriver.Chrome(executable_path=self.config['driver'])

    def login(self):
        while True:
            ok = self.find_element_by_class_name('sn-login')
            ok1 = self.find_element_by_id('J_Go')
            if ok or not ok1:
                element = self.find_element_by_class_name('sn-login')
                if element:
                    element.click()
                time.sleep(self.config['login_time'])
            else:
                break

    def buy(self):
        try:
            element = self.find_element_by_id('J_Go')
            if element:
                element.click()
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def check_select_all(self):
        try:
            self.browser.find_element_by_xpath("//div[@class='shop-info']/div[@class='cart-checkbox ']")
            return True
        except Exception as e:
            print(e)
            return False

    def select_all(self):
        element = self.browser.find_element_by_class_name('cart-checkbox')
        try:
            if element:
                element.click()
                time.sleep(1)
                return element.find_element_by_xpath('input').is_selected()
        except Exception as e:
            print(e)
            return False
        return True

    def submit_order(self):
        element = self.browser.find_element_by_class_name('go-btn')
        try:
            if element:
                element.click()
        except Exception as e:
            print(e)
            return False
        return True

    def run(self):
        self.browser.get(self.config['url'])
        self.login()
        if 'op_time' in self.config:
            try:
                print(self.config['op_time'])
                print((self.config['op_time'] - datetime.now()).microseconds)
                seconds_delta = (self.config['op_time'] - datetime.now()).total_seconds()
                if seconds_delta > 0:
                    print('wait {}s'.format(seconds_delta))
                    time.sleep(seconds_delta)
            except Exception as e:
                print(e)
        while True:
            ok = self.check_select_all()
            if ok:
                print('items are ready!')
                break
            print('items are not ready!')
            time.sleep(0.1)
        self.select_all()
        while not self.submit_order():
            ok = self.buy()
            print('buy :', ok)
            if ok:
                break
        # while True:
        #     ok = self.submit_order()
        #     if ok:
        #         break


    def find_element_by_name(self, name):
        from selenium.common.exceptions import NoSuchElementException
        try:
            element = self.browser.find_element_by_name(name)
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

    def find_element_by_id(self, id):
        from selenium.common.exceptions import NoSuchElementException
        try:
            element = self.browser.find_element_by_id(id)
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


if __name__ == '__main__':
    model = clear_cart(sys.argv[1])
    model.run()
