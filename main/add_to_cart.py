import yaml
from selenium import webdriver

class add_to_cart:

    def __init__(self, conf_name):
        self.config = yaml.load(open('conf/{}.yaml'.format(conf_name)), Loader=yaml.FullLoader)
        self.browser = webdriver.Chrome(executable_path=self.config['driver'])

    def run(self):
        self.browser.get(self.config['url'])


if __name__ == '__main__':
    model = add_to_cart('test')
    model.run()
