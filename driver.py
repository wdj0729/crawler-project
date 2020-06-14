import os
from selenium import webdriver


class Chrome:
    path = os.getcwd() + "chromedriver.exe"
    options = webdriver.ChromeOptions

    def __init__(self, visible = True):
        self.set_options()
        self.visible = visible
        self.driver = webdriver.Chrome(Chrome.path, Chrome.options)

    def set_options(self):
        if self.visible:
            Chrome.options.add_argument("window-size=1920x1080")
            Chrome.options.add_argument("disable-infobars")
            Chrome.options.add_argument("--disable-extentions")
        else:
            Chrome.options.add_argument("headless")
            Chrome.options.add_argument("window-size=1920x1080")
            Chrome.options.add_argument("disable-gpu")
            Chrome.options.add_argument("disable-infobars")
            Chrome.options.add_argument("--disable-extentions")

    def get(self, url: str) -> webdriver:
        try:
            self.driver.get(url)
            self.driver.maximize_window()
        except Exception as e:
            return e
        return self.driver
