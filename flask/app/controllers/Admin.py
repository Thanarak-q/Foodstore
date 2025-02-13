from app.controllers import ctable_mange
from app.controllers import menu_manage
from app.controllers import employee_manage

from flask import Flask, render_template
from app import app

@app.route('/admin')
def base():
    return render_template('Admin_page/base.html')