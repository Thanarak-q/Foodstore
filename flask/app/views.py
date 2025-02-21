import json
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)

# from app.controllers import table_manage
# from app.controllers import order_manage
from werkzeug.security import check_password_hash
from werkzeug.urls import url_parse
# from app import login_manager
from sqlalchemy.sql import text
from flask_login import login_user
from app import app
from app import db

import jwt
from manage import SECRET_KEY



'''
หน้า Admin
'''
from app.controllers import Admin

'''
หน้า Cashier
'''
from app.controllers import cashier

# @app.route('/test', methods=('GET', 'POST'))
# def test():
#     return render_template('test_bend.html')

# @app.route('/lab11/login', methods=('GET', 'POST'))
# def lab11_login():
#     if request.method == 'POST':
#         # login code goes here
#         email = request.form.get('email')
#         password = request.form.get('password')
#         remember = bool(request.form.get('remember'))


#         user = AuthUser.query.filter_by(email=email).first()
 
#         # check if the user actually exists
#         # take the user-supplied password, hash it, and compare it to the
#         # hashed password in the database
#         if not user or not check_password_hash(user.password, password):
#             flash('Please check your login details and try again.')
#             # if the user doesn't exist or password is wrong, reload the page
#             return redirect(url_for('lab11_login'))


#         # if the above check passes, then we know the user has the right
#         # credentials
#         login_user(user, remember=remember)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('lab11_profile')
#         return redirect(next_page)


#     return render_template('lab11/login.html')

@app.route('/table/test')
def table_test():
    return render_template('test_bend.html')

@app.route("/Order")
def order():
    return render_template('order_page/index.html')

@app.route('/menu/table/<token>', methods=['GET', 'POST'])
def menu(token):
    table_number = decode_jwt(token)
    app.logger.debug(not table_number)
    if not table_number:
        return "Invalid or expired token", 400

    if request.method == 'GET':
        # selected_items = request.form.getlist('item')  # List of selected items' ids
        # return render_template('order_summary.html', table_number=table_number, selected_items=selected_items, menu_items=menu_items)
        return render_template('test.html', table_id=table_number)

    # return render_template('menu.html', menu_items=menu_items, table_number=table_number)
    return render_template('test.html', table_id='Something wrong with your QRcode')

def decode_jwt(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded['table_number']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None





















































@app.route('/')
def home():
    return render_template('order_page/index.html')

@app.route('/index')
def index():
    return app.send_static_file('index.html')

@app.route('/crash')
def crash():
    return 1/0

@app.route('/db')
def db_connection():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return '<h1>db works.</h1>'
    except Exception as e:
        return '<h1>db is broken.</h1>' + str(e)

@app.route('/cookingroom')
def cookingroom():
    return render_template('cooking_page/base.html')
