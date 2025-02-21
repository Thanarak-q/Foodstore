# from app.controllers import ctable_mange
from app.controllers import table_manage
from app.controllers import menu_manage
from app.controllers import employee_manage
from app.controllers import order_manage

from flask import Flask, render_template
from app import app

@app.route('/cashier')
def cashier_index():
    return render_template('cashier_page/index.html')   