import json
from sqlalchemy.sql import text
from app import app
from app import db
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)
from app.controllers.role_controller import roles_required 
from flask_login import login_required
from app.models.menu import Menu

@app.route('/admin')
@roles_required('Admin')
@login_required
def dashboard():
    return render_template('Admin_page/dashboard.html')