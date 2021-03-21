from flask import Flask, request, render_template, redirect, session, g, jsonify, flash

from model import db, connect_db, User, Food,  Wine, Wineparing
from myfunc import Search_recipe, Recipe_details, Search_wine, wine_paring_for_recipe, Wine_paring_for_meal, Dish_paring_for_wine
from forms import LoginForm, SignUpForm
from sqlalchemy.exc import IntegrityError

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
# db.drop_all()
# db.create_all()

###################### Users ###########################


@app.before_request
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


@app.route('/signup', methods=['POST', 'GET'])
def sing_up():
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            user = User.register(username, password, email,
                                 first_name, last_name)
            db.session.add(user)
            db.session.commit()
            flash("User Created!", "success")

        except IntegrityError:
            flash("Username already taken", 'danger')
            flash("email is already used", 'danger')
            return render_template('signup_form.html', form=form)

        do_login(user)

        return redirect("/home")
    else:
        return render_template("signup_form.html", form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    if session[CURR_USER_KEY]:
        do_logout()
        flash("loged out successfully", "info")
        return redirect('/')


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()
    try:

        if form.validate_on_submit():
            user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/home")

        flash("Invalid credentials.", 'danger')
    except ValueError:
        flash("Invalid Password", "danger")

    return render_template('landingpage.html', form=form)


@app.route('/user/<int:id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    else:
        user = User.query.get_or_404(id)
        form = SignUpForm(obj=user)
        if form.validate_on_submit():
            user.username = form.username.data
            user.password = form.password.data
            user.email = form.email.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            db.session.add(user)
            db.session.commit()
            flash("User Details Updated", "success")
            return redirect(f'/user/{id}/edit')
        return render_template("user_edit.html", form=form)
#################### Recipes ##################


@app.route('/')
def landingpage():
    form = LoginForm()
    return render_template("landingpage.html", form=form)


@app.route('/home')
def home():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    return render_template('home.html')


@app.route('/searchrecipe/<food>')
def serach_recipe(food):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    else:
        response = Search_recipe(food)
        return jsonify(response)


@app.route('/recipedetail/<int:id>')
def recipe_detail(id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    else:
        response = Recipe_details(id)
        return render_template("recipe_details.html", recipe=response)


@app.route('/saverecipe/<int:id>')
def save_recipe(id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    else:

        response = Recipe_details(id)
        recipe = Food(dish_name=response['title'], dish_id=response['id'], description=response['description'], ingredients=response['ingredients'],
                      total_time=response['total_time'], instruction=response['instructions'], image_url=response['image'])
        db.session.add(recipe)
        db.session.commit()
        flash("Recipe is saved.", 'success')
        return redirect("/savedrecipe")


@app.route('/savedrecipe')
def recipe_lists():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    else:
        recipe_list = Food.query.all()
        return render_template("saved_recipe.html", s_recipe=recipe_list)


@app.route('/savedrecipe/details/<int:id>')
def save_recipe_details(id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    else:
        response = Recipe_details(id)
        return render_template("saved_recipe_details.html", recipe=response)


@app.route('/recipe/delete/<int:id>')
def delete_recipe(id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    else:
        del_recipe = Food.query.filter(Food.dish_id == id).first()
        db.session.delete(del_recipe)
        db.session.commit()
        return redirect('/savedrecipe')


######################## Wine ################


@app.route('/api/wineparing/<int:id>')
def wineparing_recipe(id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    else:
        response = wine_paring_for_recipe(id)
        if response:
            return jsonify(response)
        else:
            response = {
                "wineParing": "No wine is reccomended with this meal"
            }
            return jsonify(response)


@app.route('/wine')
def wine_home():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    else:
        return render_template("wine.html")


@app.route('/searchwine/<type>')
def search_wine(type):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    else:
        response = Search_wine(type)
        return jsonify(response)
