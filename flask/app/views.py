import json
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)

# from app.controllers import table_manage
# from app.controllers import order_manage
# from app import login_manager
from sqlalchemy.sql import text
from flask_login import login_required
from app.controllers.role_controller import roles_required
from app import app
from app import db

import jwt
from manage import SECRET_KEY



'''
หน้า Admin
'''
from app.controllers import Admin
from app.controllers import review_manage
'''
หน้าอื่น ๆ
'''
from app.controllers import cashier
from app.models.table import Tables
from app.controllers import review
from app.controllers import waiter
from app.controllers import cookingroom
from app.controllers import customer_table




@app.route('/')
def home():
    """Root landing page showing all available pages and login credentials"""
    return render_template('landing_page.html')

# @app.route('/index')
# def index():
#     return app.send_static_file('index.html')

# @app.route('/crash')
# def crash():
#     return 1/0

# @app.route('/db')
# @login_required
# @roles_required('Admin')
# def db_connection():
#     try:
#         with db.engine.connect() as conn:
#             conn.execute(text("SELECT 1"))
#         return '<h1>db works.</h1>'
#     except Exception as e:
#         return '<h1>db is broken.</h1>' + str(e)



