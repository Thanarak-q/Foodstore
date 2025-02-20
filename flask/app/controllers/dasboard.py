import json
from sqlalchemy.sql import text
from app import app
from app import db
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)

from app.models.menu import Menu

@app.route('/admin')
def dashboard():
    return render_template('Admin_page/dashboard.html')