from flask_bcrypt import Bcrypt
from flask import Flask, render_template, redirect, session, flash, request
from flask_app import app
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.models import recipe
from flask_app.models import user

bcrypt = Bcrypt(app)


# main page with user/new user login and reg
@app.route('/')
def user_login():
    if 'user_id' not in session:
        return render_template('home.html')
    else: return redirect ('/dashboard')

# page for when user signs in/user display page
@app.route('/dashboard')
def user_welcome():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('dash.html', user = user.User.select_id(id=session['user_id']), all_recipes = recipe.Recipe.get_all_recipes())

# action to register new user
@app.route('/register', methods=['POST'])
def user_reg():
    if not user.User.validate_user(request.form):
        return redirect('/')
    session['user_id'] = user.User.new_user(request.form)
    return redirect('/dashboard')

# action for user login
@app.route('/login', methods=['POST'])
def login():
    if not user.User.validate_email(request.form):
        return redirect ('/')
    user_sessions = user.User.select_email(request.form)
    session['user_id'] = user_sessions.id
    return redirect('/dashboard')

# logout action to clear session
@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')