# Web driver class

# import libraries
from selenium import webdriver
from time import sleep

class Driver:
    def __init__(self):
        """
        Initiate Chrome web driver.
        """
        self.driver = webdriver.Chrome()


    def get(self, url, time=1):
        """
        Go to URL provided and wait for page to load.
        """
        self.page = self.driver.get(url)
        sleep(time)
        return self.page

    def find_elements(self, xpath=""):
        """
        Returns list of elements with specified xpath.
        """
        self.elements = self.driver.find_elements_by_xpath(xpath)
        return self.elements