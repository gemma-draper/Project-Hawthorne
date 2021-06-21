#%%
# Class for scraping data from Tipsy Bartender

from driver_class import Driver

class Tipsy():
    def __init__(self):
        # Instantiate the driver
        self.d = Driver()
        self.d.get('https://tipsybartender.com/drinks/all/')
        #self.d.quit()
        self.drinks_categories = []
        self.category_dict = {}
        self.all_drinks = []
    
    def get_category_urls(self):
        all_categories = self.d.find_elements('//div[contains(@class, "subcollection-list")]/a')
        for category in all_categories:
            self.category_dict['url'] = category.get_attribute('href')
            self.category_dict['category'] = category.find_element_by_xpath('.//h5').text
            self.drinks_categories.append(self.category_dict.copy())
            #self.d.quit()   
        return self.drinks_categories

    def get_drinks_urls(self):
        drink_info = {}

        for category in self.drinks_categories:
            self.d.get(category['url'])
            # get the number of pages from the nav bar
            number_of_pages = int(self.d.get_text('//nav[@aria-label="Page navigation"]//li[last()-1]'))
    
        for i in range(1,number_of_pages+1):
            # iterate through all the pages in this category
            self.d.get(category['url'] + f'/page/{i}/')
            #get all the drinks on this page
            all_drinks_on_this_page = self.d.find_elements('//div[contains(@class, "drink-card")]/a')
        
    
        for drink in all_drinks_on_this_page:
            drink_info['category'] = category['category']
            drink_info['name'] = drink.find_element_by_xpath('.//span').text
            drink_info['url'] = drink.get_attribute('href')
            self.all_drinks.append(drink_info.copy())

        #self.d.quit()
        return self.all_drinks



# test the functions.
# tipsy = Tipsy()

# category_info = tipsy.get_category_urls()
# drinks_info = tipsy.get_drinks_urls()

# for dictionary in drinks_info:
#     # go to each recipe url
#     tipsy.d.get(dictionary['url'])
#%%
#init
d = Driver()
d.get('http://allrecipes.co.uk/recipes/drink-recipes.aspx')
drink_recipes_element = d.find_element('//*[text()="Drink recipes"]')
all_recipes_url = drink_recipes_element.find_element_by_xpath('..').get_attribute('href')
drinks_from_all_recipes = []

# get drink names and urls
d.get(all_recipes_url)
page_count = d.find_element('//div[contains(@class, "pageCount")]').text
clean_page_count = int(page_count.split()[-1])
base_url = "http://allrecipes.co.uk/recipes/drink-recipes.aspx?page="

for i in range(clean_page_count):
    d.get(base_url + str(i+1))
    #get all the names and urls
    drinks_on_this_page = d.find_elements('//div[contains(@class, "row recipe")]')
    for drink in drinks_on_this_page:
        drink_info = {}
        name_node = drink.find_element_by_xpath('.//a[@itemprop="name"]')
        drink_info['name'] = name_node.text
        drink_info['url'] = name_node.get_attribute('href')
        drinks_from_all_recipes.append(drink_info.copy())

print(drinks_from_all_recipes)
#%%

import re

drink_dict = drinks_from_all_recipes[1]
d.get(drink_dict['url'])

def get_ingredients(drink_dict=drink_dict):
    all_ingredients = d.find_elements('//*[@itemprop="ingredients"]')
    for i in range(len(all_ingredients)):
        key = "ingredient_" + str(i)
        value = all_ingredients[i].text
        drink_dict[key] = value
    return drink_dict

#get yield
def get_yield(drink_dict=drink_dict):
    recipe_yield = d.find_element('//*[@itemprop="recipeYield"]/span')
    drink_dict['recipe_yield'] = recipe_yield.text
    return drink_dict

#get description
def get_description(drink_dict=drink_dict):
    recipe_description = d.find_element('//p[@itemprop="description"]')
    drink_dict['description'] = recipe_description.text
    return drink_dict

#get method
def get_method(drink_dict=drink_dict):
    full_method =  d.find_elements('//*[@itemprop="recipeInstructions"]/li')
    for i in range(len(full_method)):
        key = "step_" + str(i)
        value = full_method[i].find_element_by_xpath('./span').text
        drink_dict[key] = value
    return drink_dict

def clean_star_rating(messy=messy_star_rating):
    """Takes a string containing star rating.
    Removes all non-numeric chars.
    Returns star rating as float.
    """
    messy = re.sub('[^0-9]', "", messy)
    if len(messy) == 2:
        clean = float(messy[0] + "." + messy[1])
    else:
        clean = float(messy)
    return clean

#get star rating
def get_n_reviews_and_rating(drink_dict=drink_dict):
    star_rating_box = d.find_element('//span[contains(@class, "mediumStar")]')
    messy_star_rating = star_rating_box.get_attribute('class')
    messy_n_reviews = star_rating_box.find_element_by_xpath('../*[contains(@id, "Count")]').text

    drink_dict['star_rating'] = clean_star_rating()
    drink_dict['n_reviews'] = int(messy_n_reviews.lstrip('( ').rstrip(') '))
    return drink_dict

drink_dict = get_ingredients()
drink_dict = get_yield()
drink_dict = get_description()
drink_dict = get_method() 
drink_dict = get_n_reviews_and_rating()


from pprint import pprint
pprint(drink_dict)

#%%
# %%
