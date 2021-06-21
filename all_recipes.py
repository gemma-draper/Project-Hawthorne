import re
from pprint import pprint
from driver_class import Driver

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
