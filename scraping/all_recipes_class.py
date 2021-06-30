#%%
import re
import json
from driver_class import Driver
import pandas as pd
from pprint import pprint

class All_recipes_scraper():
    def __init__(self):
        # initialise the web driver
        self.d = Driver()
        # initialise the list of drinks
        self.drinks = []

    def get_basic_info(self):
        """
        Returns name, url and id for every drink on site as list of dicts.
        """
        # go to the drinks recipes cover page
        self.d.get('http://allrecipes.co.uk/recipes/drink-recipes.aspx')
        # Find the heading element which has text "Drink recipes"
        drink_recipes_element = self.d.find_element('//*[text()="Drink recipes"]')
        # get the href from its parent node
        all_recipes_url = drink_recipes_element.find_element_by_xpath('..').get_attribute('href')
        # initialise id. Starts at 1 instead of 0 as 0's are interpreted as null by SQL later on in pipeline.
        id = 1
        # go to the url we retrieved
        self.d.get(all_recipes_url)
        # find the element with the total number of pages, and clean it to get an integer.
        page_count = self.d.find_element('//div[contains(@class, "pageCount")]').text
        clean_page_count = int(page_count.split()[-1])
        # set the base url. We will join a number to this to iterate through all pages of drinks recipes.
        base_url = "http://allrecipes.co.uk/recipes/drink-recipes.aspx?page="
        # iterate through all pages of drinks recipes
        for i in range(clean_page_count):
            # go to the page
            self.d.get(base_url + str(i+1))
            # get all drinks on the page
            drinks_on_this_page = self.d.find_elements('//div[contains(@class, "row recipe")]')
            # iterate through them, creating a dict for each drink and adding id, name and url to each dict. Append to list.
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
