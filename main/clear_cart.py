# -*- coding: <encoding name> -*- : # -*- coding: utf-8 -*-
import yaml
import time
import sys
from selenium import webdriver

class clear_cart:

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

        for oper in self.config['oper'].split(';'):
            element = self.find_by_link_text(oper)
            print(element)
            if not element:
                continue
            print('click')
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
        self.browser.execute_script("arguments[0].click();", element)
        # from selenium.common.exceptions import ElementClickInterceptedException
        # try:
        #     element.click()
        # except ElementClickInterceptedException as e:
        #     print(e)
        #     self.browser.execute_script("arguments[0].click();", element)


if __name__ == '__main__':
    model = clear_cart('test')
    model.run()
