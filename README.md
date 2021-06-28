# Project Hawthorne

A Python web scraper for collecting cocktail recipes from user submitted recipe websites.

This project is under development. Parts of the project marked with ✔️ are complete. Parts marked with 🚧 are under development.

## Planned work

### Data Pipielines Project

I plan to scrape drink recipes from the following sites:
* allrecipes.co.uk ✔️
* bbcgoodfood.com 🚧
* tipsybartender.com 🚧
* food52.com 🚧

Work packages:
* Driver() class created ✔️
* Script written with functions to scrape all drinks from allrecipes.com ✔️
* All_recipes_scraper() class working 🚧
* Data collected from allrecipes.com ✔️
* Allrecipes.com data clean ✔️
* Data pipeline to AWS RDS PostgreSQL database complete ✔️
* bbcgoodfood.com scraper 🚧
* tipsybartender.com scraper 🚧
* food52.com scraper 🚧
* 
## Libraries & dependencies

Libraries required: [selenium](https://selenium-python.readthedocs.io/), pandas, re, json, pprint, sqlalchemy and psycopg2.

Selenium requires [Chromedriver](https://chromedriver.chromium.org/).

## Motivation

Project Hawthorne is a data piplines project for [AiCore](https://www.theaicore.com/). The data collected using this scraper will later be used to train a ML model.

## Feedback

Feedback on this project is welcome. Find me on [LinkedIn](https://www.linkedin.com/in/gemma-l-draper/).
