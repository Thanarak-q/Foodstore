import json
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)

# from app.controllers import table_manage
from werkzeug.security import check_password_hash
from werkzeug.urls import url_parse
# from app import login_manager
from sqlalchemy.sql import text
from flask_login import login_user
from app import app
from app import db




'''
หน้า Admin
'''
from app.controllers import Admin

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





















































@app.route('/')
def home():
    return "Flask says 'Hello world!'"

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

@app.route('/lab04')
def lab04_bootstrap():
    return app.send_static_file('lab04_bootstrap.html')

@app.route('/lab10', methods=('GET', 'POST'))
def lab10_phonebook():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
        id_ = result.get('id', '')
        validated = True
        validated_dict = dict()
        valid_keys = ['firstname', 'lastname', 'phone']

        # validate the input
        for key in result:
            app.logger.debug(f"{key}: {result[key]}")
            # screen of unrelated inputs
            if key not in valid_keys:
                continue

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value

        if validated:
            app.logger.debug('validated dict: ' + str(validated_dict))
            # if there is no id: create a new contact entry
            if not id_:
                entry = Contact(**validated_dict)
                app.logger.debug(str(entry))
                db.session.add(entry)
            # if there is an id already: update the contact entry
            else:
                contact = Contact.query.get(id_)
                contact.update(**validated_dict)

            db.session.commit()

        return lab10_db_contacts()
    return app.send_static_file('test.html')

@app.route("/lab10/contacts")
def lab10_db_contacts():
    contacts = []
    db_contacts = Contact.query.all()

    contacts = list(map(lambda x: x.to_dict(), db_contacts))
    app.logger.debug("DB Contacts: " + str(contacts))

    return jsonify(contacts)

@app.route('/lab10/remove_contact', methods=('GET', 'POST'))
def lab10_remove_contacts():
    app.logger.debug("LAB10 - REMOVE")
    if request.method == 'POST':
        result = request.form.to_dict()
        id_ = result.get('id', '')
        try:
            contact = Contact.query.get(id_)
            db.session.delete(contact)
            db.session.commit()
        except Exception as ex:
            app.logger.error(f"Error removing contact with id {id_}: {ex}")
            raise
    return lab10_db_contacts()

