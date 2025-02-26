import json
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)

from app import app
from app import db
from app import login_manager
from sqlalchemy.sql import text
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse

from app.models.employee import Employee

@app.route('/login' ,methods=['POST', "GET"])
def login():
    if request.method == 'POST':
        # login code goes here
        username = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))


        user = Employee.query.filter_by(username=username).first()
 
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the
        # hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            # if the user doesn't exist or password is wrong, reload the page
            return render_template('Admin_page/login.html')


        # if the above check passes, then we know the user has the right
        # credentials
        login_user(user, remember=remember)

        if current_user.role == 'Admin':
            return render_template('Admin_page/dashboard.html')
        elif current_user.role == 'Chef':
            return render_template('cooking_page/base.html')
        elif current_user.role == 'Waiter':
            return render_template('waiter_page/base.html')
        elif current_user.role == 'Cashier':
            return render_template('cashier_page/index.html')
        else:
            return 'Who r u?'

    return render_template('Admin_page/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('Admin_page/login.html')

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our
    # user table, use it in the query for the user
    return Employee.query.get(int(user_id))
