"""Flask web interface for food nutritional information."""

import json
import os
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from food import Food

app = Flask(__name__)
app.secret_key = "food_secret_key_2024"

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

# Full list of 922 foods scraped from infocalories.fr
FOOD_LIST = [
    "abricot-fruit", "abricot-sec", "abricots-au-sirop", "accras-morue", "acerola", "agar-agar",
    "agneau-cotelette-grillee", "agneau-epaule", "agneau-foie", "agneau-gigot-roti", "aiglefin", "aiguillette-canard",
    "aiguillette-poulet", "ail", "ailes-poulet", "airelles", "amande", "amandes-poudre",
    "americano", "ananas", "ananas-au-sirop", "anchois", "anchois-huile", "andouille-vire",
    "andouillette", "aneth", "anguille", "anisette", "araignee-boeuf", "armagnac",
    "artichaut", "artichaut-coeur", "asperge", "aubergine", "avocat", "babybel",
    "bacon", "baguette", "baie-goji", "bambou", "banana-split", "banane",
    "banane-plantain", "bar", "basilic", "batavia", "batonnet-crabe", "bavette-boeuf",
    "bcaa", "beaufort", "becasse", "beignet", "beignet-confiture", "betterave-rouge-cuite",
    "beurre", "beurre-allege", "beurre-cacahuetes", "beurre-leger", "beurre-sale", "bicarbonate-k",
    "biche", "biere", "biere-blonde", "biere-brune", "biere-light", "biere-sans-alcool",
    "bifteck-boeuf", "bifteck-hache-15", "bifteck-hache-5", "big-mac", "bigorneau", "biscottes",
    "bisque-homard", "blanc-de-dinde", "blanc-de-poulet", "blanc-oeuf", "ble-germe", "blettes-cuites",
    "bleu-de-bresse", "blinis", "boeuf", "boeuf-bourguignon", "boeuf-carottes", "boeuf-tranche-subway",
    "bonbel", "bonbons", "boss-bacon-kfc", "boudin-blanc", "boudin-noir", "boudoir",
    "bouillon-cube-boeuf", "boulettes-de-viande", "boulghour", "bounty-chocolat-lait", "bounty-noir", "bourbon",
    "boursin", "box-master-original-kfc", "brandy", "brazer-kfc", "bresaola", "bretzel",
    "brick", "brie", "brioche", "brochet", "brocoli-cuit", "brownie",
    "brugnon", "buche-glacee", "burritos", "cabillaud", "cabillaud-pane-frit", "cacahuetes",
    "cacao-poudre", "cafe-liegeois", "cafe-noir", "caille", "cake", "calamars-frits",
    "calamars-natures", "calisson", "calvados", "camembert", "campari-americano", "canard-laque",
    "canard-roti", "cancoillotte", "cannelloni", "cantal", "cappuccino", "capres",
    "caramel", "carotte", "carottes-cuites", "carpaccio-boeuf", "carpe", "carrelet",
    "caseine", "cassis", "cassoulet", "caviar", "caviar-aubergines", "celeri-branche",
    "celeri-rave", "cepes", "cerf", "cerises", "cervelas", "chair-saucisse",
    "champagne", "champagne-brut", "champignons", "champignons-noirs", "champignons-paris", "chanterelle",
    "chantilly-legere", "chaource", "chapelure", "chataigne", "chataigne-grillee", "chaussee-aux-moines",
    "chausson-pommes", "cheddar", "cheese-cake", "cheeseburger-mcdo", "chevre-frais", "chevre-sec",
    "chevreuil-roti", "chewing-gum", "chili-con-carne", "chipolata", "chips", "chocolat",
    "chocolat-blanc", "chocolat-chaud", "chocolat-lait", "chocolat-lait-noisettes", "chocolat-liegeois", "chocolat-noir",
    "chocolat-poudre", "chocolatine", "chorizo", "chou", "chou-blanc", "chou-chinois",
    "chou-creme", "chou-de-bruxelles", "chou-farci", "chou-fleur", "chou-rouge", "chou-vert",
    "choucroute-garnie", "chouquette", "ciboulette", "cidre", "cidre-brut", "cigarette-russe",
    "citron", "citron-vert", "citrouille", "civet-lapin", "civet-sanglier", "clafoutis",
    "clams", "clementine", "coca-cola", "coca-cola-light", "coeur-palmier", "cognac",
    "coing", "cointreau", "colin", "collagene", "collagene-marin", "compote-pommes",
    "comte", "concombre", "confiture", "confiture-moins-sucree", "congre", "cookies",
    "coppa", "coquille-saint-jacques", "cordon-bleu", "corn-flakes", "corned-beef", "cornes-de-gazelle",
    "cornichon", "cosmopolitan", "cote-de-porc", "cottage-cheese", "coulis-tomates", "coulommiers",
    "courge", "courgette", "couscous", "crabe", "crabe-boite", "cracotte",
    "cranberry", "creatine", "creme-anglaise", "creme-brulee", "creme-caramel", "creme-cassis",
    "creme-chantilly", "creme-de-riz", "creme-fraiche", "creme-glacee", "creme-patissiere", "crepes",
    "crevettes", "crevettes-roses", "croissant", "croissant-amandes", "croissant-chocolat", "croquant-amandes",
    "croque-monsieur", "croquettes-poisson", "crottin", "cruesli", "crumble", "cube-bouillon",
    "cuisses-de-poulet", "curacao", "curry", "danette-chocolat", "danette-vanille", "datte",
    "deluxe-patatoes", "dinde", "donuts", "dorade", "dragee", "durian",
    "eau", "eau-de-vie", "ebly", "echalote", "eclair-au-chocolat", "eclair-cafe",
    "eclair-vanille", "ecrevisse", "edam", "edulcorant", "eglefin", "emmental",
    "enchiladas", "encornet", "endive", "endive-cuite", "endive-jambon", "entrecote",
    "epinards", "escalope-cordon-bleu", "escalope-milanaise", "escalope-poulet", "escargot-beurre", "escargots-natures",
    "espadon", "extravaganza-dominos", "faisselle", "fajitas", "falafels", "fanta",
    "farce-porc", "farfalle", "farine-avoine", "farine-ble", "farine-mais", "farine-patate-douce",
    "feijoada", "ferrero-rocher", "feta", "feves-cuites", "figues", "figues-seches",
    "filet-cabillaud", "financier", "fish-and-chips", "flageolets", "flammekueche", "flan-oeufs",
    "flan-patissier", "fletan", "flocons-avoine", "foie-genisse", "foie-gras", "foie-volaille",
    "fondue-bourguignonne", "fondue-savoyarde", "fougasse", "fourme-ambert", "fourme-montbrison", "fraises",
    "framboise", "frites", "fromage-abondance", "fromage-blanc", "fromage-livarot", "fromage-rape",
    "fromage-tete", "fruit-de-la-passion", "fruit-du-dragon", "fruit-or", "fruits-confits", "gainers",
    "galak", "galantine", "galette-de-riz", "galette-des-rois", "galette-st-michel", "gambas-grillees",
    "gaspacho", "gateau-au-yaourt", "gateau-savoie", "gateau-semoule", "gaufre-sucre", "gelee-coings",
    "gelee-royale", "genoise", "germe-ble", "germe-soja", "gesiers", "gin",
    "gin-fizz", "gingembre", "gingembre-confit", "girolle", "glace", "glace-chocolat",
    "glace-fraise", "glace-vanille", "gnocchi", "gorgonzola", "gouda", "goyave",
    "goyave-conserve", "graines-de-sesame", "graines-tournesol", "granola", "gratin-dauphinois", "grenade",
    "grenadine", "groseille", "gruyere", "guacamole", "hachis-parmentier", "haddock",
    "hamburger-mcdo", "hampe-boeuf", "hareng", "hareng-fume", "haricot-vert", "haricots-blancs",
    "haricots-rouges", "harissa", "homard", "hot-dog", "hot-wings-kfc", "houmous",
    "huile-arachide", "huile-colza", "huile-friture", "huile-olive", "huile-soja", "huile-tournseol",
    "huitres", "ice-tea", "igname", "ile-flottante", "irish-coffee", "isolat-caseine",
    "isostar", "jalebi", "jambon-beurre", "jambon-blanc", "jambon-cru", "jambon-dinde",
    "jambon-paris", "jambon-sans-nitrite", "jambon-volaille", "jambonneau-cuit", "jardiniere-legumes", "jus-abricot",
    "jus-ananas", "jus-carotte", "jus-de-citron", "jus-orange", "jus-pamplemousse", "jus-peche",
    "jus-poire", "jus-pomme", "jus-pruneaux", "jus-raisin", "jus-tomate", "kaki",
    "kebab", "kefir", "kefta-agneau", "kelloggs", "ketchup", "kinder-bueno",
    "kinder-country", "kinder-delice", "kinder-maxi", "kinder-pingui", "kinder-surprise", "kiri-creme",
    "kiri-gouter", "kirsch", "kit-kat", "kiwi", "knack", "knacki",
    "krisprolls", "krunchy-kfc", "kub-or-maggi", "lait", "lait-amande", "lait-avoine",
    "lait-chevre", "lait-chocolate", "lait-coco", "lait-concentre-sucre", "lait-ecreme", "lait-ecreme-poudre",
    "lait-entier", "lait-epeautre", "lait-noisette", "lait-sans-lactose", "lait-soja", "laitue",
    "langoustine", "langue-boeuf", "langues-chat", "lapin", "lard", "lardons",
    "lasagnes", "lentilles", "lentilles-cuites", "levure-boulanger", "lieu", "lievre-civet",
    "limonade", "litchi", "loukoums", "m&ms", "maasdam", "macaron",
    "macaronis", "macedoine", "mache-salade", "madeleine", "madere", "magnum-amande",
    "magnum-chocolat", "magret-de-canard", "mahi-mahi", "mai-tai", "mais", "mais-en-boite",
    "maizena", "maki-saumon", "maki-thon", "mandarine", "mangue", "maquereaux",
    "margarine", "margarita", "margherita", "marron-glace", "marrons", "mars",
    "marshmallows", "martini", "mascarpone", "mayonnaise", "mayonnaise-allegee", "mcchiken",
    "mechoui", "melon", "merguez", "meringue", "merlan-frit", "merlu",
    "miel", "miel-pops", "mille-feuille", "mimolette", "mirabelle", "modele",
    "moelleux-chocolat", "mojito", "mont-dor", "morbier", "mortadelle", "morue",
    "moules-frites", "moules-marinieres", "mousse-canard", "mousse-chocolat", "mousse-foie", "mousseux",
    "moutarde", "moutarde-dijon", "mouton", "mozzarella", "muesli", "muffin",
    "munster", "mures", "muscat", "museau-porc", "myrtilles", "nachos",
    "napolitain", "navets-cuits", "nectar-abricot", "nectarine", "nem", "nescafe-cappuccino",
    "nescafe-expresso", "nesquik", "nestea", "noisettes", "noix", "noix-cajou",
    "noix-de-coco", "noix-du-bresil", "noix-grenoble", "noix-macadamia", "noix-pecan", "noix-st-jacques",
    "nougat", "nougat-glace", "nouilles-chinoises", "nuggets", "nuoc-nam", "nutella",
    "oasis-orange", "oeuf-au-plat", "oeuf-coque", "oeuf-dur", "oeuf-dur-mayonnaise", "oeuf-lump",
    "oeuf-mimosa", "oeufs-brouilles", "oie-rotie", "oignon-cru", "olive", "olive-noire",
    "olive-verte", "omelette", "omelette-fromage", "omelette-norvegienne", "orange", "orangina",
    "oreo", "origan", "oseille-cuite", "oursin", "ovomaltine", "paella",
    "pain", "pain-au-chocolat", "pain-au-lait", "pain-azyme", "pain-baguette", "pain-brioche",
    "pain-burger", "pain-complet", "pain-epices", "pain-grille", "pain-lardons", "pain-levain",
    "pain-mie", "pain-mie-grille", "pain-raisin", "pain-seigle", "pain-son", "pain-viennois",
    "palmiers", "pamplemousse", "pancakes", "pancakes-proteines", "pancetta", "panini",
    "papaye", "paris-brest", "parmentier-boeuf", "parmesan", "pasteque", "pastis",
    "patate", "patate-douce", "pate-amande", "pate-brisee", "pate-campagne", "pate-de-foie",
    "pate-en-croute", "pate-feuilletee", "pate-imperial", "pate-porc", "pate-sablee", "pates",
    "pates-fruits", "paupiette-veau", "pave-affinois", "peches", "pepperoni", "pepperoni-dominos",
    "peppina-dominos", "persil", "petit-suisse", "petits-pois", "pignons-pin", "piments-rouges",
    "pina-colada", "pistaches", "pizza-bacon-dominos", "pizza-boeuf-pepperoni-dominos", "pizza-cannibale-dominos", "pizza-chorizo",
    "pizza-figue-chevre-dominos", "pizza-forestiere", "pizza-fromage", "pizza-fromages", "pizza-hawaienne", "pizza-hypnotika-dominos",
    "pizza-indienne-dominos", "pizza-louisiane-pizza-hut", "pizza-montagnarde-pizza-hut", "pizza-orientale", "pizza-pesto-verde-dominos", "pizza-provencale-pizza-hut",
    "pizza-queen-pizza-hut", "pizza-regina", "pizza-salame-piccante-dominos", "pizza-saumon-ecosse-dominos", "pizza-savoyarde-dominos", "pizza-street-kebab-dominos",
    "pizza-supreme-pizza-hut", "pizza-vegetarienne-pizza-hut", "pizzas", "poire", "poireau", "pois-casses",
    "pois-chiches", "poisson-pane", "poisson-perche", "poivrons", "pomme", "pommes-de-terre",
    "porridge", "potiron", "poulet-entier", "poulet-pane", "pringles", "pruneaux",
    "puree", "puree-mousline", "quality-street", "quatre-quart", "quenelles", "quetsche",
    "quiche-lorraine", "quinoa", "quinoa-bio", "raclette", "radis-rouge", "raisin",
    "raisin-noir", "raisins-secs", "rascasse", "ratatouille", "ravioles", "raviolis-boeuf",
    "reblochon", "religieuse", "rhubarbe-cuite", "rhum-blanc", "ricore-lait", "ricotta",
    "rillettes-oie", "rillettes-porc", "rillettes-saumon", "rillettes-volaille", "ris-veau", "risotto-champignons",
    "riz", "riz-au-lait", "riz-basmati", "riz-cantonais", "riz-complet", "riz-complet-bio",
    "riz-cru", "rocher-suchard-lait", "rognons", "rondele", "roquefort", "roquette",
    "rosette-lyon", "rouleau-de-printemps", "roussette", "rouy", "royal-bacon", "royal-deluxe-macdonald",
    "rutabaga", "sable-saint-michel", "saint-agur", "saint-felicien", "saint-marcellin", "saint-moret",
    "saint-nectaire", "salade-cesar", "salade-de-fruits", "salade-russe", "salade-verte", "salami",
    "salsifis", "samoussa", "sandre", "sandwich-club-subway", "sandwich-dinde-subway", "sandwich-italien-subway",
    "sandwich-jambon-subway", "sandwich-melt-subway", "sandwich-spicy-italien-subway", "sardine", "sardine-huile", "sauce-aigre-douce",
    "sauce-aioli", "sauce-algerienne", "sauce-barbecue", "sauce-bearnaise", "sauce-bechamel", "sauce-bolognaise",
    "sauce-bourguignonne", "sauce-cocktail", "sauce-mayonnaise", "sauce-nuoc-mam", "sauce-pesto", "sauce-poivre",
    "sauce-romesco", "sauce-salsa", "sauce-samourai", "sauce-soja", "sauce-tartare", "sauce-tomate",
    "sauce-vinaigrette", "saucisse-francfort", "saucisse-morteau", "saucisse-seche", "saucisse-strasbourg", "saucisses-lentilles",
    "saucisson", "saucisson-brioche", "saumon", "saumon-fume", "savane", "schweppes",
    "semoule", "semoule-cuite", "shake-proteines", "sirop-agave", "sirop-anis", "sirop-erable",
    "sirop-grenadine", "sirop-menthe", "skyr", "snickers", "soja-boire", "sole",
    "sorbets", "soupe-aux-choux", "soupe-legume", "soupe-lentilles", "soupe-miso", "soupe-oignon",
    "soupe-poisson", "soupe-tomate", "spaghetti", "spaghetti-bolognaise", "spaghetti-tomate", "steak-boeuf",
    "steak-de-cheval", "steak-hache", "steak-tartare", "sucre-en-poudre", "sucre-morceaux", "sucre-roux",
    "sundae", "supplement-omega-3", "surimi", "sushis", "taboule", "tacos",
    "tacos-boeuf", "tacos-poulet", "tagliatelles", "tajine-poulet", "tapas", "tapenade",
    "tarama", "tartare", "tarte-alsacienne", "tarte-aux-fraises", "tarte-aux-fruits", "tarte-champignons",
    "tarte-chevre-epinard", "tarte-chocolat", "tarte-citron", "tarte-fruits", "tarte-oignon", "tarte-pommes",
    "tartiflette", "tenders-kfc", "tequila", "terrine-canard", "terrine-de-campagne", "terrine-legume",
    "thon", "thon-huile", "tiramisu", "toblerone", "tofu", "tomate",
    "tomate-cerise", "tomates-farcies", "tomme-savoie", "topinambour", "tortilla", "tortilla-chips",
    "tournedos-boeuf", "tower-original-kfc", "travers-porc", "tripes-caen", "truffes-chocolat", "truite",
    "tuiles-aux-amandes", "turbot", "turron", "twix", "tzatziki", "vache-qui-rit",
    "vacherin", "veau", "vegetaline", "veggie-delite-subway", "vermicelle-riz", "vermouth",
    "viande-grisons", "viande-porc", "viennetta", "viennois", "vin-blanc", "vin-blanc-cassis",
    "vin-blanc-mousseux", "vin-rose", "vin-rouge", "vinaigre", "vinaigre-balsamique", "vodka",
    "vodka-orange", "wasa", "weetabix", "whey-proteine", "whisky", "whisky-coca",
    "whopper-burger-king", "yaourt-aux-fruits", "yaourt-grecque", "yaourt-lait-brebis", "yaourt-lait-entier", "yaourt-nature",
    "yaourt-nature-sucre", "yaourt-soja", "zeste-citron", "zlabia",
]


def load_users():
    """Load users from JSON file."""
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    """Save users to JSON file."""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def login_required(f):
    """Decorator to protect routes that require authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


@app.route("/")
def index():
    """Redirect to dashboard or login."""
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page."""
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        users = load_users()
        if username in users and check_password_hash(users[username], password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        error = "Identifiant ou mot de passe incorrect."
    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registration page."""
    error = None
    success = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm", "")

        if not username or not password:
            error = "Tous les champs sont obligatoires."
        elif len(password) < 4:
            error = "Le mot de passe doit faire au moins 4 caractères."
        elif password != confirm:
            error = "Les mots de passe ne correspondent pas."
        else:
            users = load_users()
            if username in users:
                error = f"Le nom d'utilisateur '{username}' est déjà pris."
            else:
                users[username] = generate_password_hash(password)
                save_users(users)
                success = f"Compte '{username}' créé ! Vous pouvez vous connecter."

    return render_template("register.html", error=error, success=success)


@app.route("/logout")
def logout():
    """Logout and redirect to login."""
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    """Main dashboard with food list."""
    return render_template("dashboard.html", foods=FOOD_LIST)


@app.route("/api/food/<food_name>")
@login_required
def api_food(food_name):
    """API endpoint returning food nutritional info as JSON."""
    try:
        food = Food()
        food.retrieve_food_infos(food_name)
        return jsonify({
            "name": food.get_name(),
            "calories": food.get_calories(),
            "fat": food.get_fat(),
            "carbs": food.get_carbs(),
            "proteins": food.get_proteins(),
            "is_fat": food.is_fat(),
        })
    except ConnectionError as e:
        return jsonify({"error": str(e)}), 404


if __name__ == "__main__":
    app.run(debug=True)
