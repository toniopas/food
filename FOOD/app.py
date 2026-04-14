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

# Predefined list of foods available on infocalories.fr
FOOD_LIST = [
    "tomate", "avocat", "amande", "pomme", "banane", "carotte", "brocoli",
    "epinard", "poulet", "saumon", "oeuf", "lait", "fromage", "yaourt",
    "riz", "pates", "pain", "beurre", "huile-olive", "noix", "lentille",
    "pois-chiche", "thon", "crevette", "fraise", "orange", "raisin",
    "concombre", "poivron", "oignon"
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
