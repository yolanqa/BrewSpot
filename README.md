# BrewSpot

Python app that scrapes and manages the best cafes in the city based on your preferences.


## Description


models/cafe.py - this file is the base for this project, contains the attributes and any other file that has to work with coffeeshops imports the Cafe class from here;



scraper/cafe_scraper.py - this file is the scraping part, here the application takes information from websites and creates objects and returns a list with those objects;



collection/cafe_collection.py - this file takes the list of cafe objects from cafe_scraper and implements the filters;



storage/file_manager.py - this file saves the objects into a JSON and then loads those information back into our application, this is useful because we have to read data from the JSON and to do the scraping part only once;
