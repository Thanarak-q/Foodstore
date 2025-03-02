from flask import Flask, render_template, request
from flask_login import login_required
from app.controllers.role_controller import roles_required 

from app import app




@app.route('/cashier')
@login_required
@roles_required('Admin', 'Cashier')
def cashier_index():
    return render_template('cashier_page/index.html')



@app.route('/cashier/qrcode')
@login_required
@roles_required('Admin', 'Cashier')
def qrcode():
    table_id = request.args.get('table_id')
    qrcode = request.args.get('qrcode')
    return render_template('cashier_page/qrcode.html', table_id=table_id, qrcode=qrcode)



@app.route('/cashier/invoice')
@login_required
@roles_required('Admin', 'Cashier')
def invoice():
    table_id = request.args.get('table_id')
    payment_method = request.args.get('payment_method')
    print(payment_method)
    return render_template('cashier_page/invoice.html', table_id=table_id, payment_method=payment_method)
