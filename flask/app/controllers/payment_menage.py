import json
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)

from app import app
from app import db
from sqlalchemy.sql import text
from flask_login import login_required, current_user
from app.controllers.role_controller import roles_required 
from app.models.store import Store
from app.models.table import Tables
from app.models.order import Order
from app.models.payment import Payment
from app.models.menu import Menu
from manage import SECRET_KEY
import math
import jwt
import qrcode
import datetime
import io
import base64
from promptpay import qrcode as pp_qrcode


@app.route('/payment/get_all_payment')
def payment_list():
    db_payment = Payment.query.all()
    payments = list(map(lambda x: x.to_dict(), db_payment))
    payments.sort(key=(lambda x: x['payment_id']))
    return jsonify(payments)


@app.route('/payment/create', methods=('GET', 'POST'))
@login_required
@roles_required('Admin', 'Cashier')
def payment_create():
    app.logger.debug("Payment - CREATE")
    if request.method == 'POST':
        result = request.form.to_dict()

        validated = True
        valid_keys = ['payment_method', 'payment_time', 'amount', 'table_id']
        table_id = result.get('table_id', '')
        validated_dict = dict()
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
            try:
                temp = Payment(**validated_dict)
                db.session.add(temp)
                change_order_status(table_id)
                table = Tables.query.get(table_id)
                table.update_status('Available')
                qrcode = gennerate_qrcode(table.table_id, table.count)
                table.change_qrcode(qrcode)
                
                db.session.commit()
                
            except Exception as ex:
                app.logger.error(f"Error create new order: {ex}")
                raise
            
    return payment_list()

def change_order_status(table_id):
    db_order = db.session.query(Order).filter(Order.table_id == table_id and Order.status != 'Paid').all() 
    orders = list(map(lambda x: x.to_dict(), db_order))
    for order in db_order:
        order.update_status('Paid')

def gennerate_qrcode(id, count):
    token = generate_jwt(id, count)
    img = qrcode.make(f'http://localhost:56733/menu/table/{token}') # Must to change to menu select url
    type(img)  # qrcode.image.pil.PilImage
    img.save(f"app/static/qrcode/{id}.png")
    return f"app/static/qrcode/{id}.png"

def generate_jwt(table_number, count):
    expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=48)
    payload = {
        'table_number': table_number,
        'exp': expiration_time,
        'count' : count
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

@app.route('/payment/update', methods=('GET', 'POST'))
@login_required
@roles_required('Admin')
def payment_update():
    app.logger.debug("Payment - UPDATE")
    if request.method == 'POST':
        result = request.form.to_dict()

        validated = True
        valid_keys = ['payment_id', 'table_id', 'payment_method', 'payment_time', 'amount']
        validated_dict = dict()
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
            try:
                payment = Payment.query.get(validated_dict['payment_id'])
                payment.update(
                    payment_method=validated_dict['payment_method'],
                    payment_time=validated_dict['payment_time'],
                    amount=validated_dict['amount']
                )
                db.session.commit()
                
            except Exception as ex:
                app.logger.error(f"Error create new order: {ex}")
                raise
            
    return payment_list()

@app.route('/payment/delete', methods=('GET', 'POST'))
@login_required
@roles_required('Admin')
def payment_delete():
    app.logger.debug("Payment - DELETE")
    if request.method == 'POST':
        if current_user.role != 'Admin':
            return 'You are not Admin'
        
        result = request.form.to_dict()

        validated = True
        valid_keys = ['payment_id']
        validated_dict = dict()
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
            try:
                payment = Payment.query.get(validated_dict['payment_id'])
                payment.update_status('Disable')
                db.session.commit()
                
            except Exception as ex:
                app.logger.error(f"Error create new order: {ex}")
                raise
            
    return payment_list()

@app.route('/payment/create_slip', methods=('GET', 'POST'))
@login_required
@roles_required('Admin', 'Cashier')
def slip_create():
    app.logger.debug("Payment - CREATE SLIP")
    if request.method == 'POST':
        result = request.form.to_dict()
        table_id = result.get('table_id', '')
        app.logger.debug(table_id)
        db_order = db.session.query(Order).filter((Order.table_id == table_id) & (Order.status != 'Paid')).all() 
        orders = list(map(lambda x: x.to_dict(), db_order))
        menu_list = dict()
        sum_list = dict()
        subtotal = 0
        store = get_store_dict()
        for order in orders:
            subtotal += order['total_price']
            menu_list = merge_dict(menu_list, order['menu_list'])

        for menu_id in menu_list:
            menu = get_menu_dict(menu_id)
            sum_list[menu['name']] = {'price' : menu_list[menu_id] * menu['price'],
                                      'price_per_unit': menu['price'],
                                      'amount': menu_list[menu_id]}
    
        vat = subtotal * store['vat'] / 100
        temp = {'vat_7%': vat, 'total' : subtotal, 'sum_price': sum_list, 'vat%': store['vat']}
        app.logger.debug(temp)
        return temp
    
@app.route('/payment/customer')
def customer_view():
    result = request.form.to_dict()
    table_id = result.get('table_id', '')
    app.logger.debug(table_id)
    db_order = db.session.query(Order).filter((Order.table_id == table_id) & (Order.status != 'Paid')).all() 
    orders = list(map(lambda x: x.to_dict(), db_order))
    menu_list = dict()
    sum_list = dict()
    subtotal = 0
    store = get_store_dict()
    for order in orders:
        subtotal += order['total_price']
        menu_list = merge_dict(menu_list, order['menu_list'])

    for menu_id in menu_list:
        menu = get_menu_dict(menu_id)
        sum_list[menu['name']] = {'price' : menu_list[menu_id] * menu['price'],
                                    'price_per_unit': menu['price'],
                                    'amount': menu_list[menu_id]}

    vat = subtotal * store['vat'] / 100
    total = math.floor(subtotal * (100 + store['vat']) / 100)
    qr_data = pp_qrcode.generate_payload(store['Promptpay_id'], amount=total)
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(f'app/static/qrcode_pp/{table_id}.png')


    temp = {'vat_7%': vat, 'total' : subtotal, 'sum_price': sum_list, 'vat%': store['vat'], 'qrcode': f'app/static/qrcode_pp/{table_id}.png'}
    # app.logger.debug(temp)
    return temp

def merge_dict(A, B):
    temp = dict(A)
    for b in B:
        if b in temp:
            temp[b] += B[b]
        else:
            temp[b] = B[b]
    return temp

def get_menu_dict(id):
    db_menu = Menu.query.get(id)
    menu = db_menu.to_dict()
    return menu

def get_store_dict():
    db_store = Store.query.get(1)
    store = db_store.to_dict()
    return store