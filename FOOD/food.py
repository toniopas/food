import requests
from bs4 import BeautifulSoup
import csv
import re

# ── Variable globale : URL de base du site ──────────────────────────────────
URL_BASE = "https://www.infocalories.fr/calories/calories-{}.php"
SEUIL_GRAS = 20  # seuil en % pour considérer un aliment comme gras


class Aliment:
    """ Classe représentant un aliment avec ses valeurs nutritionnelles """

    __nom       = None
    __calories  = None
    __lipides   = None
    __glucides  = None
    __proteines = None

    # ── Getters ─────────────────────────────────────────────────────────────

    def get_nom(self):
        """ Retourne le nom de l'aliment """
        return self.__nom

    def get_calories(self):
        """ Retourne les calories (kcal) """
        return self.__calories

    def get_lipides(self):
        """ Retourne les lipides (g) """
        return self.__lipides

    def get_glucides(self):
        """ Retourne les glucides (g) """
        return self.__glucides

    def get_proteines(self):
        """ Retourne les protéines (g) """
        return self.__proteines

    # ── Setters ─────────────────────────────────────────────────────────────

    def set_nom(self, nom):
        """ Définit le nom de l'aliment """
        self.__nom = nom

    def set_calories(self, calories):
        """ Définit les calories """
        self.__calories = calories

    def set_lipides(self, lipides):
        """ Définit les lipides """
        self.__lipides = lipides

    def set_glucides(self, glucides):
        """ Définit les glucides """
        self.__glucides = glucides

    def set_proteines(self, proteines):
        """ Définit les protéines """
        self.__proteines = proteines

    # ── Méthodes principales ─────────────────────────────────────────────────

    def recuperer_infos(self, nom_aliment):
        """
        Récupère les informations nutritionnelles depuis infocalories.fr
        en fonction du nom de l'aliment donné.

        - L'URL est construite depuis la variable globale URL_BASE
        - Vérifie que la requête HTTP a réussi (code 200)
        - Lève une exception si la requête échoue
        """
        self.set_nom(nom_aliment)

        # Construction de l'URL : "avocat" → calories-avocat.php
        slug = nom_aliment.lower().replace(" ", "-")
        url  = URL_BASE.format(slug)

        # Requête HTTP
        reponse = requests.get(url, timeout=10)

        # Vérification du succès de la requête
        if reponse.status_code != 200:
            raise ConnectionError(
                f"Échec de la requête pour '{nom_aliment}' "
                f"(HTTP {reponse.status_code}) — URL : {url}"
            )

        # Analyse du HTML
        soupe = BeautifulSoup(reponse.text, "html.parser")
        texte = soupe.get_text()

        # Extraction des valeurs nutritionnelles
        def extraire(pattern):
            correspondance = re.search(pattern, texte, re.IGNORECASE)
            return float(correspondance.group(1).replace(",", ".")) if correspondance else None

        self.set_calories(extraire(r"(\d+[\.,]?\d*)\s*Kcal"))
        self.set_proteines(extraire(r"(\d+[\.,]?\d*)\s*g\s+de\s+prot[eé]ines"))
        self.set_glucides(extraire(r"(\d+[\.,]?\d*)\s*g\s+de\s+glucides"))
        self.set_lipides(extraire(r"(\d+[\.,]?\d*)\s*g\s+de\s+lipides"))

    def afficher_infos(self):
        """
        Affiche les informations nutritionnelles sous forme de tableau :

        ------------------------------------------------
        nom        calories   lipides  glucides  proteines
        avocat     360.0      37.0     2.0       5.0
        ------------------------------------------------
        """
        separateur = "-" * 60
        print(separateur)
        print(f"{'nom':<15}{'calories':<12}{'lipides':<10}{'glucides':<10}{'proteines'}")
        print(
            f"{str(self.__nom):<15}"
            f"{str(self.__calories):<12}"
            f"{str(self.__lipides):<10}"
            f"{str(self.__glucides):<10}"
            f"{str(self.__proteines)}"
        )
        print(separateur)

    def sauvegarder_csv(self, nom_fichier):
        """
        Sauvegarde les informations nutritionnelles dans un fichier CSV.
        Utilise 'with' pour l'ouverture du fichier.
        """
        with open(nom_fichier, mode="w", newline="", encoding="utf-8") as fichier_csv:
            writer = csv.writer(fichier_csv)
            # En-tête
            writer.writerow(["nom", "calories", "lipides", "glucides", "proteines"])
            # Données
            writer.writerow([
                self.__nom,
                self.__calories,
                self.__lipides,
                self.__glucides,
                self.__proteines,
            ])
        print(f"✅  Données sauvegardées dans '{nom_fichier}'")

    def est_gras(self):
        """
        Retourne True si les lipides représentent plus de SEUIL_GRAS %
        des calories totales (1g de lipides = 9 kcal).
        Retourne False si les données ne sont pas disponibles.
        """
        if self.__calories is None or self.__lipides is None or self.__calories == 0:
            return False

        calories_lipides = self.__lipides * 9           # 1g lipides = 9 kcal
        pourcentage_gras = (calories_lipides / self.__calories) * 100

        return pourcentage_gras > SEUIL_GRAS


# ── Programme principal ──────────────────────────────────────────────────────
if __name__ == "__main__":

    nom = input("Entrez le nom d'un aliment : ")
    aliment = Aliment()

    try:
        aliment.recuperer_infos(nom)
        aliment.afficher_infos()
        aliment.sauvegarder_csv(f"{nom}.csv")
        print(f"   Aliment gras (> {SEUIL_GRAS}% lipides) : {aliment.est_gras()}")

    except ConnectionError as e:
        print(f"❌  Erreur : {e}")
        print(f"   💡 Astuce : vérifiez l'orthographe ou essayez avec un tiret (ex: blanc-de-poulet)")