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