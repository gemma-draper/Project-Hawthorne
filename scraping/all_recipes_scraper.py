import re
import json
from driver_class import Driver
import pandas as pd
from pprint import pprint
d = Driver()

def get_basic_info(d=d):
    """
    Returns name, url and id for every drink on site as list of dicts.
    """
    d.get('http://allrecipes.co.uk/recipes/drink-recipes.aspx')
    drink_recipes_element = d.find_element('//*[text()="Drink recipes"]')
    all_recipes_url = drink_recipes_element.find_element_by_xpath('..').get_attribute('href')
    drinks = []
    id = 1
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
            drink_info['id'] = id
            id += 1
            drink_info['name'] = name_node.text
            drink_info['url'] = name_node.get_attribute('href')
            drinks.append(drink_info.copy())
    return drinks

# get and print basic info for more drinks
drinks_from_all_recipes = get_basic_info()
pprint(drinks_from_all_recipes)

# save the basic data
with open('basic_data.txt', 'w') as f:
    json.dump(drinks_from_all_recipes, f)

# define some more functions
def get_ingredients(drink_dict, d=d):
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
def get_yield(drink_dict, d=d):
    """
    Scrapes recipe yield.
    Takes drink_dict, returns it with recipe_yield.
    """
    recipe_yield = d.find_element('//*[@itemprop="recipeYield"]/span')
    drink_dict['recipe_yield'] = recipe_yield.text
    return drink_dict

#get description
def get_description(drink_dict, d=d):
    """
    Scrapes recipe description.
    Takes drink_dict, returns it with description.
    """
    recipe_description = d.find_element('//p[@itemprop="description"]')
    drink_dict['description'] = recipe_description.text
    return drink_dict

#get method
def get_method(drink_dict, d=d):
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
def get_n_ratings_and_rating(drink_dict, d=d):
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

def get_time(drink_dict, d=d):
    """
    Scrapes preparation time.
    Takes drink_dict and returns it with prep_time.
    """
    prep_time = d.find_element('//div[contains(@class,"stat1")]/span')
    try:
        drink_dict['prep_time'] = prep_time.text
    except AttributeError:
        drink_dict['prep_time'] = ""
    return drink_dict

def get_everything(list=drinks_from_all_recipes, d=d):
    """
    Calls fuctions to get ingredients, yield, description, method, ratings, and prep time.
    Returns list of dicts, each dict containing data for one drink.
    """
    for drink_dict in list[968:]:
        d.get(drink_dict['url'])

        drink_dict = get_ingredients(drink_dict)
        drink_dict = get_yield(drink_dict)
        drink_dict = get_description(drink_dict)
        drink_dict = get_method(drink_dict) 
        drink_dict = get_n_ratings_and_rating(drink_dict)
        drink_dict = get_time(drink_dict)
        pprint(drink_dict)
        
    return list

# run the get_everything function
drinks_from_all_recipes = get_everything()

# convert to a dataframe 
drinks_df = pd.DataFrame(drinks_from_all_recipes)
# set id col as index
drinks_df.set_index('id', inplace=True)
# expand the ingredients and methods dictionaries
drinks_df = pd.concat([drinks_df, pd.json_normalize(drinks_df['ingredients'])], axis=1)
drinks_df = pd.concat([drinks_df, pd.json_normalize(drinks_df['method'])], axis=1)
# drop the dictionaries
drinks_df = drinks_df.drop(['ingredients', 'method'], axis=1)

# convert df to json
for_json = drinks_df.to_json(orient='columns')

# export to json
with open('all_recipes_df_data.txt', 'w') as f:
    json.dump(for_json, f)
