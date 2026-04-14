"""Flask web interface for food nutritional information."""

from flask import Flask, render_template, request
from food import Food

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """Home page: display nutritional info for a searched food."""
    food_data = None
    error = None
    food_name = ""

    if request.method == "POST":
        food_name = request.form.get("food_name", "").strip()
        if food_name:
            try:
                food = Food()
                food.retrieve_food_infos(food_name)
                food_data = {
                    "name": food.get_name(),
                    "calories": food.get_calories(),
                    "fat": food.get_fat(),
                    "carbs": food.get_carbs(),
                    "proteins": food.get_proteins(),
                    "is_fat": food.is_fat(),
                }
            except ConnectionError as e:
                error = str(e)

    return render_template("index.html", food=food_data, error=error, food_name=food_name)


if __name__ == "__main__":
    app.run(debug=True)
