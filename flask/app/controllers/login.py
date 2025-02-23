import json
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)

from app import app
from app import db
from sqlalchemy.sql import text
from flask_login import login_user, current_user, logout_user

@app.route('/login')
def login():
        
    return render_template('Admin_page/login.html')
