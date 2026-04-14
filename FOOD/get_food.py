from food import Food
import argparse

import sys
print("Running script...")

parser = argparse.ArgumentParser("Food Informations")
parser.add_argument('-f', '--food', help="your food name", default='tomate')

# use the parser to get all the needed arguments
args = parser.parse_args()

# retrieve and display food infos
food = Food()
food.retrieve_food_infos(args.food)
food.display_food_infos()

# save the displayed infos to a csv file
food.save_to_csv_file(f"{args.food}.csv")
