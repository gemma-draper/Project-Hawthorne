# Web driver class
# import libraries
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep

from selenium.webdriver.remote import webelement

class Driver:
    def __init__(self):
        """
        Initiate Chrome web driver.
        """
        self.driver = webdriver.Chrome()


    def get(self, url:str, time=1):
        """
        Go to URL provided and wait for page to load.
        """
        page = self.driver.get(url)
        sleep(time)
        return page
    
    def quit(self):
        self.driver.quit()
        return

    def find_elements(self, xpath:str):
        """
        Returns list of elements with specified xpath.
        If NoSuchElementException returns empty list.
        """
        try:
            elements = self.driver.find_elements_by_xpath(xpath)
            
        except NoSuchElementException:
            elements = []
        
        return elements

    def find_element(self, xpath:str):
        """
        Returns an element with specified xpath.
        """
        try:
            element = self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            element = []
        return element

    # def find_element_by_type(self,type:str):
    #     """
    #     Returns element with specified type.
    #     """
    #     element = self.driver.find_element_by_xpath(f"//[@type=\'{type}\']")
    #     return element
       

    def get_text(self, xpath:str):
        """
        Returns text from the element specified
        """
        try:
            text = self.driver.find_element_by_xpath(xpath).text
        except NoSuchElementException:
            text = ""
        return text
