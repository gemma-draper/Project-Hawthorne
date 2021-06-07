# Web scraper for tipsybartender.com
# %%
import pandas as pd

# initialise the web driver
from selenium import webdriver
from time import sleep
driver = webdriver.Chrome()

# Set the URL. Sleep to allow site to load.
driver.get('https://tipsybartender.com/drinks/all/')
sleep(1)

# get all category names and urls.
# store in a list of dicts.
drinks_categories = []
category_dict = {}
all_categories = driver.find_elements_by_xpath('//div[contains(@class, "subcollection-list")]/a')

for category in all_categories:
    category_dict['url'] = category.get_attribute('href')
    category_dict['category'] = category.find_element_by_xpath('.//h5').text
    drinks_categories.append(category_dict.copy())

all_drinks = pd.DataFrame()
drink_info = {}

for category in drinks_categories:
    # go to the url and wait
    driver.get(category['url'])
    sleep(1)
    # get the number of pages from the nav bar
    number_of_pages = int(driver.find_element_by_xpath('//nav[@aria-label="Page navigation"]//li[last()-1]').text)
    
    for i in range(1,number_of_pages+1):
        # iterate through all the pages in this category
        driver.get(category['url'] + f'/page/{i}/')
        #get all the drinks on this page
        all_drinks_on_this_page = driver.find_elements_by_xpath('//div[contains(@class, "drink-card")]/a')
        
        for drink in all_drinks_on_this_page:
            drink_info['category'] = category['category']
            drink_info['name'] = drink.find_element_by_xpath('.//span').text
            drink_info['url'] = drink.get_attribute('href')
            all_drinks = all_drinks.append(drink_info,ignore_index=True)
            

        
driver.quit()
#%%
all_drinks.head()

# pokemons = driver.find_elements_by_xpath(‘/html/body/div[4]/section[5]/ul/li’)
# pokemons_list = []
# for main_pokemon in pokemons:
#     id = main_pokemon.find_element_by_xpath(‘.//p’).text
#     print(id)
#     name = main_pokemon.find_element_by_xpath(‘.//h5’).text
#     print(name)
#     link = main_pokemon.find_element_by_xpath(‘.//a’)
#     url = link.get_attribute(‘href’)
#     print(url)
#     pokemons_list.append({‘id’:id,‘name’:name,‘url’:url})
# for pokemon_dict in pokemons_list:
#     driver.get(pokemon_dict[‘url’])
#     pokemon_dict[‘img’] = driver.find_element_by_xpath(‘/html/body/div[4]/section[3]/div[1]/div[1]/div/img’).get_attribute(‘src’)
#     # blue_box = driver.find_element_by_xpath(‘/html/body/div[4]/section[3]/div[2]/div/div[5]‘)
#     blue_box = driver.find_element_by_xpath(‘//div[contains(@class, “pokemon-ability-info”)]‘)
#     attributes = blue_box.find_elements_by_xpath(‘//li’)
#     for attr in attributes:
#         key = blue_box.find_element_by_xpath(‘.//span[1]‘).text.lower()
#         pokemon_dict[key] = blue_box.find_element_by_xpath(‘.//span[2]‘).text
#     print(pokemon_dict)
#     print(f’Details: img>{pokemon_dict[“img”]}‘)
#     print(f’Details: height>{pokemon_dict[“height”]}’)
#     sleep(1)
# driver.quit()
# # %%
# # %%