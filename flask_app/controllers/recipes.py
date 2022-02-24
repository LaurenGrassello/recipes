from flask import Flask, render_template, redirect, session, flash, request
from flask_app import app
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.models import user
from flask_app.models import recipe


# displays recipe
@app.route('/recipes/<int:id>')
def recipes(id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id': id 
    }
    return render_template("recipe.html", all_recipes = recipe.Recipe.select_recipe_id(data), user = user.User.select_id(id=session['user_id']))


# route to add new recipe
@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect ('/')
    return render_template('new_recipe.html')


# action to add new recipe
@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect ('/')
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect ('/recipes/new')
    recipe_data = {
        'user_id': session['user_id'], 
        'name': request.form['name'],
        'description': request.form['description'],
        'under_30_min': int(request.form['under_30_min']),
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made']
        }
    recipe.Recipe.new_recipe(recipe_data)
    return redirect ('/dashboard')


@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id 
    }
    recipes = recipe.Recipe.select_recipe_id(data)
    return render_template('edit_recipe.html', recipes = recipes)


@app.route('/recipes/edit/complete/<int:id>', methods=['POST'])
def update_complete(id):
    if 'user_id' not in session:
        return redirect ('/')
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect (f'/recipes/edit/{id}')
    data = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'under_30_min': int(request.form['under_30_min']),
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'id': id
    }
    recipe.Recipe.edit_recipe(data)
    return redirect('/dashboard')


@app.route("/recipes/delete/<int:id>")
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id': id
    }
    recipe.Recipe.delete_recipe(data)
    return redirect('/dashboard')







