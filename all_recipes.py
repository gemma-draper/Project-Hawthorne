
import re
import json
from pprint import pprint
from driver_class import Driver
from pprint import pprint

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

#%%

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
def get_ingredients(drink_dict):
    """
    Scrapes drink ingredients.
    Takes drink_dict, returns drink_dict key and value for each ingredient.
    """
    all_ingredients = d.find_elements('//*[@itemprop="ingredients"]')
    ingredients_dict = {}
    for i in range(len(all_ingredients)):
        key = "ingredient_" + str(i)
        value = all_ingredients[i].text
        ingredients_dict[key] = value
    drink_dict['ingredients'] = ingredients_dict
    return drink_dict

#get yield
def get_yield(drink_dict):
    """
    Scrapes recipe yield.
    Takes drink_dict, returns it with recipe_yield.
    """
    recipe_yield = d.find_element('//*[@itemprop="recipeYield"]/span')
    drink_dict['recipe_yield'] = recipe_yield.text
    return drink_dict

#get description
def get_description(drink_dict):
    """
    Scrapes recipe description.
    Takes drink_dict, returns it with description.
    """
    recipe_description = d.find_element('//p[@itemprop="description"]')
    drink_dict['description'] = recipe_description.text
    return drink_dict

#get method
def get_method(drink_dict):
    """
    Scrapes recipe method.
    Takes drink_dict, returns it with drink_dict['method'] = method_dict.
    """
    full_method =  d.find_elements('//*[@itemprop="recipeInstructions"]/li')
    method_dict = {}
    for i in range(len(full_method)):
        key = "step_" + str(i)
        value = full_method[i].find_element_by_xpath('./span').text
        method_dict[key] = value
    drink_dict['method'] = method_dict
    return drink_dict

def clean_star_rating(messy):
    """
    Takes a string containing star rating.
    Removes all non-numeric chars.
    Returns star rating as float.
    """
    messy = re.sub('[^0-9]', "", messy)
    if len(messy) == 2:
        clean = float(messy[0] + "." + messy[1])
    else:
        clean = float(messy)
    return clean

#get star rating and number of reviews
def get_n_ratings_and_rating(drink_dict):
    """
    Scrapes star rating and number of ratings.
    Takes drink_dict and returns it with star_rating and n_ratings.
    """
    star_rating_box = d.find_element('//span[contains(@class, "mediumStar")]')
    
    messy_star_rating = star_rating_box.get_attribute('class')
    messy_n_ratings = star_rating_box.find_element_by_xpath('../*[contains(@id, "Count")]').text

    drink_dict['star_rating'] = clean_star_rating(messy_star_rating)
    drink_dict['n_ratings'] = int(messy_n_ratings.lstrip('( ').rstrip(') '))
    return drink_dict

def get_time(drink_dict):
    """
    Scrapes preparation time.
    Takes drink_dict and returns it with prep_time.
    """
    prep_time = d.find_element('//div[contains(@class,"stat1")]/span')
    drink_dict['prep_time'] = prep_time
    return drink_dict
#%%

def get_everything(list=drinks_from_all_recipes):
    count = 0
    for drink_dict in list:
        d.get(drink_dict['url'])

        drink_dict = get_ingredients(drink_dict)
        drink_dict = get_yield(drink_dict)
        drink_dict = get_description(drink_dict)
        drink_dict = get_method(drink_dict) 
        drink_dict = get_n_ratings_and_rating(drink_dict)
        drink_dict = get_time(drink_dict)
        print(count)
        count += 1
    return list

#%%
drinks_from_all_recipes = get_everything()
import json
with open('all_recipes_data.txt', 'w') as f:
    json.dump(drinks_from_all_recipes, f, skipkeys=True)