#%%
import re
import json
from driver_class import Driver
import pandas as pd
from pprint import pprint

class All_recipes_scraper():
    def __init__(self):
        self.d = Driver()

    def get_basic_info(self):
        """
        Returns name, url and id for every drink on site as list of dicts.
        """
        self.d.get('http://allrecipes.co.uk/recipes/drink-recipes.aspx')
        drink_recipes_element = self.d.find_element('//*[text()="Drink recipes"]')
        all_recipes_url = drink_recipes_element.find_element_by_xpath('..').get_attribute('href')
        self.drinks = []
        id = 1
        self.d.get(all_recipes_url)
        page_count = self.d.find_element('//div[contains(@class, "pageCount")]').text
        clean_page_count = int(page_count.split()[-1])
        base_url = "http://allrecipes.co.uk/recipes/drink-recipes.aspx?page="
        for i in range(clean_page_count):
            self.d.get(base_url + str(i+1))
            #get all the names and urls
            drinks_on_this_page = self.d.find_elements('//div[contains(@class, "row recipe")]')
            for drink in drinks_on_this_page:
                drink_info = {}
                name_node = drink.find_element_by_xpath('.//a[@itemprop="name"]')
                drink_info['id'] = id
                id += 1
                drink_info['name'] = name_node.text
                drink_info['url'] = name_node.get_attribute('href')
                self.drinks.append(drink_info.copy())
        return self.drinks

a_r_scraper = All_recipes_scraper()
basic_info = a_r_scraper.get_basic_info()
# %%
