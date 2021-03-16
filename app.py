from flask import Flask, request, render_template, redirect, session, g, jsonify
from model import db, connect_db, User, Food, Cocktails, Wine, Wineparing
from myfunc import Search_recipe, Recipe_details, Search_wine, Wine_paring_for_meal, Dish_paring_for_wine
import keys
import os
import requests

CURR_USER_KEY = keys.CURR_USER_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', keys.database)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get(keys.SECRET_KEY, 'SQLALCHEMY')

connect_db(app)

""" api setups:
using keywords: https://api.spoonacular.com/recipes/search?query=pasta&apiKey={keys.s_api}

recipe's details: https://api.spoonacular.com/recipes/{id}/information?apiKey={keys.s_api}
get ingdrents by id: https://api.spoonacular.com/recipes/715538/ingredientWidget.json?apiKey=1edd0ae07bdd44df9d7fbde570f1134a

wine:
keywords:https://api.spoonacular.com/food/wine/recommendation?wine=merlot&number=2&apiKey=1edd0ae07bdd44df9d7fbde570f1134a
Dish_Paring_For_Wine: https://api.spoonacular.com/food/wine/dishes?wine=malbec&apiKey={keys.s_api}
Wine_Paring_For_Food: https://api.spoonacular.com/food/wine/pairing?food=steak&apiKey={keys.s_api}

cocktails:


"""


def add_user_to_g():
    """ If user is logged in, add user to FLASK GLOBAL."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/')
def landingpage():
    return render_template("home.html")
