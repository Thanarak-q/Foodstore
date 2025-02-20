# from app.controllers import ctable_mange
from app.controllers import table_manage
from app.controllers import menu_manage
from app.controllers import employee_manage

from app.controllers.Dashboard import Revenue

from flask import (jsonify, render_template,
                   request, url_for, flash, redirect)
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from app import app
# from app import login_manager
from app import db
# from app.models.employee import AuthUser

@app.route('/admin')
def base():
    return render_template('Admin_page/base.html')

# @app.route('/admin/login', methods=('POST', 'GET'))
# def admin_login():
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
#             return redirect(url_for('admin_login'))


#         # if the above check passes, then we know the user has the right
#         # credentials
#         login_user(user, remember=remember)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('admin_profile')
#         return redirect(next_page)


#     return render_template('admin_test/login.html')

# @app.route('/admin/signup', methods=('GET', 'POST'))
# def admin_signup():
#     if request.method == 'POST':
#         result = request.form.to_dict()
#         app.logger.debug(str(result))
 
#         validated = True
#         validated_dict = {}
#         valid_keys = ['email', 'name', 'password']

#         # if len(result['password']) < 4 or len(result['password']) > 22:
#         #     validated = False

#         # validate the input
#         for key in result:
#             app.logger.debug(str(key)+": " + str(result[key]))
#             # screen of unrelated inputs
#             if key not in valid_keys:
#                 continue


#             value = result[key].strip()
#             if not value or value == 'undefined':
#                 validated = False
#                 break
#             validated_dict[key] = value
#             # code to validate and add user to database goes here
#         app.logger.debug("validation done")
#         if validated:
#             app.logger.debug('validated dict: ' + str(validated_dict))
#             email = validated_dict['email']
#             name = validated_dict['name']
#             password = validated_dict['password']
#             # if this returns a user, then the email already exists in database
#             user = AuthUser.query.filter_by(email=email).first()


#             if user:
#                 # if a user is found, we want to redirect back to signup
#                 # page so user can try again
#                 flash('Email address already exists')
#                 return redirect(url_for('admin_signup'))


#             # create a new user with the form data. Hash the password so
#             # the plaintext version isn't saved.
#             app.logger.debug("preparing to add")
#             avatar_url = gen_avatar_url(email, name)
#             new_user = AuthUser(email=email, name=name,
#                                 password=generate_password_hash(
#                                     password, method='sha256'),
#                                 avatar_url=avatar_url)
#             # add the new user to the database
#             db.session.add(new_user)
#             db.session.commit()


#         return redirect(url_for('admin_login'))
#     return render_template('admin_test/signup.html')

# @app.route('/admin/profile')
# @login_required
# def admin_profile():
#     return render_template('admin_test/profile.html')

# @app.route('/admin')
# def admin_index():
#    return render_template('admin_test/index.html')

# def gen_avatar_url(email, name):
#     bgcolor = generate_password_hash(email, method='sha256')[-6:]
#     color = hex(int('0xffffff', 0) -
#                 int('0x'+bgcolor, 0)).replace('0x', '')
#     lname = ''
#     temp = name.split()
#     fname = temp[0][0]
#     if len(temp) > 1:
#         lname = temp[1][0]


#     avatar_url = "https://ui-avatars.com/api/?name=" + \
#         fname + "+" + lname + "&background=" + \
#         bgcolor + "&color=" + color
#     return avatar_url




# @app.route('/admin/logout')
# @login_required
# def admin_logout():
#     logout_user()
#     return redirect(url_for('admin_index'))

# @login_manager.user_loader
# def load_user(user_id):
#     # since the user_id is just the primary key of our
#     # user table, use it in the query for the user
#     return AuthUser.query.get(int(user_id))
