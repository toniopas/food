import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://www.infocalories.fr/calories/calories-{}.php"
FAT_THRESHOLD = 20  # seuil en % pour considérer un aliment comme gras


class Food:

    __name      = None
    __calories  = None
    __fat       = None   # lipides
    __carbs     = None   # glucides
    __proteins  = None   # protéines


    def get_name(self):
        """ Retourne le nom de l'aliment """
        return self.__name

    def get_calories(self):
        """ Retourne les calories (kcal) """
        return self.__calories

    def get_fat(self):
        """ Retourne les lipides (g) """
        return self.__fat

    def get_carbs(self):
        """ Retourne les glucides (g) """
        return self.__carbs

    def get_proteins(self):
        """ Retourne les protéines (g) """
        return self.__proteins


    def set_name(self, name):
        """ Définit le nom de l'aliment """
        self.__name = name

    def set_calories(self, calories):
        """ Définit les calories """
        self.__calories = calories

    def set_fat(self, fat):
        """ Définit les lipides """
        self.__fat = fat

    def set_carbs(self, carbs):
        """ Définit les glucides """
        self.__carbs = carbs

    def set_proteins(self, proteins):
        """ Définit les protéines """
        self.__proteins = proteins


    def retrieve_food_infos(self, food_name):

        self.set_name(food_name)

        slug = food_name.lower().replace(" ", "-")
        url  = BASE_URL.format(slug)

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            raise ConnectionError(
                f"Échec de la requête pour '{food_name}' "
                f"(HTTP {response.status_code}) — URL : {url}"
            )

        soup = BeautifulSoup(response.text, "html.parser")

        import re

        text = soup.get_text()

        def extraire(pattern):
            match = re.search(pattern, text, re.IGNORECASE)
            return float(match.group(1).replace(",", ".")) if match else None

        self.set_calories(extraire(r"(\d+[\.,]?\d*)\s*Kcal"))
        self.set_proteins(extraire(r"(\d+[\.,]?\d*)\s*g\s+de\s+prot[eé]ines"))
        self.set_carbs(extraire(r"(\d+[\.,]?\d*)\s*g\s+de\s+glucides"))
        self.set_fat(extraire(r"(\d+[\.,]?\d*)\s*g\s+de\s+lipides"))

    def display_food_infos(self):

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

        with open(file_name, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            # En-tête
            writer.writerow(["name", "calories", "fat", "carbs", "proteins"])
            # Données
            writer.writerow([
                self.__name,
                self.__calories,
                self.__fat,
                self.__carbs,
                self.__proteins,
            ])
        print(f"✅  Données sauvegardées dans '{file_name}'")

    def is_fat(self):

        if self.__calories is None or self.__fat is None or self.__calories == 0:
            return False

        calories_from_fat = self.__fat * 9          # 1g lipides = 9 kcal
        fat_percentage    = (calories_from_fat / self.__calories) * 100

        return fat_percentage > FAT_THRESHOLD


if __name__ == "__main__":

    nom = input("Entrez le nom d'un aliment : ")
    food = Food()

    try:
        food.retrieve_food_infos(nom)
        food.display_food_infos()
        food.save_to_csv_file(f"{nom}.csv")
        print(f"   Aliment gras (> {FAT_THRESHOLD}% lipides) : {food.is_fat()}")

    except ConnectionError as e:
        print(f"❌  Erreur : {e}")