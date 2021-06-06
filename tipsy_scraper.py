# Web scraper for tipsybartender.com
# %%
# initialise the web driver
from selenium import webdriver
from time import sleep
driver = webdriver.Chrome()

# Set the URL. Sleep to allow sit to load.
driver.get('https://tipsybartender.com/drinks/all/')
sleep(2)

drinks_categories = []
category_dict = {}
all_categories = driver.find_elements_by_xpath('//div[contains(@class, "subcollection-list")]/a')

for category in all_categories:
    category_dict['url'] = category.get_attribute('href')
    category_dict['category'] = category.find_element_by_xpath('.//h5').text
    drinks_categories.append(category_dict.copy())

# print(drinks_categories)


driver.quit()

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