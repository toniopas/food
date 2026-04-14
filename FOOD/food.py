"""Module for scraping and managing food nutritional information."""

import csv
import re

import requests
from bs4 import BeautifulSoup

# Global variable : base URL of the website
BASE_URL = "https://www.infocalories.fr/calories/calories-{}.php"
FAT_THRESHOLD = 20  # fat threshold in % to consider a food as fat


class Food:
    """ class food """
    __name     = None
    __calories = None
    __fat      = None
    __carbs    = None
    __proteins = None

    def get_name(self):
        """ function : get the food name """
        return self.__name

    def set_name(self, name):
        """ function : set the food name """
        self.__name = name

    def get_calories(self):
        """ function : get the property named calories of the food """
        return self.__calories

    def set_calories(self, calories):
        """ function : set the property named calories of the food """
        self.__calories = calories

    def get_fat(self):
        """ function : get the property named fat of the food """
        return self.__fat

    def set_fat(self, fat):
        """ function : set the property named fat of the food """
        self.__fat = fat

    def get_carbs(self):
        """ function : get the property named carbs of the food """
        return self.__carbs

    def set_carbs(self, carbs):
        """ function : set the property named carbs of the food """
        self.__carbs = carbs

    def get_proteins(self):
        """ function : get the property named proteins of the food """
        return self.__proteins

    def set_proteins(self, proteins):
        """ function : get the property named proteins of the food """
        self.__proteins = proteins

    def retrieve_food_infos(self, food_name):
        """ function : scrap the properties of the food from a website given its name
        
        - think of making the URL a global variable
        - check whether the request succeed before trying to parse the payload
        - if not succesfull, raise an error
        
        """
        self.set_name(food_name)

        # Build URL from global variable
        slug = food_name.lower().replace(" ", "-")
        url  = BASE_URL.format(slug)

        # HTTP request
        response = requests.get(url, timeout=10)

        # Fallback: try singular form if plural returns 404
        if response.status_code == 404 and slug.endswith("s"):
            slug = slug[:-1]
            url = BASE_URL.format(slug)
            response = requests.get(url, timeout=10)

        # Check request success
        if response.status_code != 200:
            raise ConnectionError(
                f"Aliment '{food_name}' introuvable sur le site. "
                f"Essayez avec un autre nom (ex: singulier, sans accent)."
            )

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        # Extract nutritional values with regex
        def extract(pattern):
            match = re.search(pattern, text, re.IGNORECASE)
            return float(match.group(1).replace(",", ".")) if match else None

        self.set_calories(extract(r"(\d+[\.,]?\d*)\s*Kcal"))
        self.set_proteins(extract(r"(\d+[\.,]?\d*)\s*g\s+de\s+prot[eé]ines"))
        self.set_carbs(extract(r"(\d+[\.,]?\d*)\s*g\s+de\s+glucides"))
        self.set_fat(extract(r"(\d+[\.,]?\d*)\s*g\s+de\s+lipides"))

    def display_food_infos(self):
        """ function : display the properties of the food 
        the outlook should be similar to this:
                ------------------------------------------------
                name	    calories	fat	    carbs	proteins
                tomate	    21.0		0.3	    4.6	    0.8
                ------------------------------------------------
        """
        separator = "-" * 56
        print(separator)
        print(f"{'name':<15}{'calories':<12}{'fat':<10}{'carbs':<10}{'proteins'}")
        print(
            f"{str(self.__name):<15}"
            f"{str(self.__calories):<12}"
            f"{str(self.__fat):<10}"
            f"{str(self.__carbs):<10}"
            f"{str(self.__proteins)}"
        )
        print(separator)

    def save_to_csv_file(self, file_name):
        """ function : save the properties of the food in a csv file 
        - use function with for file opening
        """
        with open(file_name, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["name", "calories", "fat", "carbs", "proteins"])
            writer.writerow([
                self.__name,
                self.__calories,
                self.__fat,
                self.__carbs,
                self.__proteins,
            ])
        print(f"Saved to '{file_name}'")

    def is_fat(self):
        """ function : return true or false whether the food has more than 20% of fat 
        - define a fat threshold and write the function accordingly
        """
        if self.__calories is None or self.__fat is None or self.__calories == 0:
            return False

        calories_from_fat = self.__fat * 9
        fat_percentage    = (calories_from_fat / self.__calories) * 100

        return fat_percentage > FAT_THRESHOLD
