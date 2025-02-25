import json
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)

from app import app
from app import db
from sqlalchemy.sql import text
import datetime

from app.models.table import Tables
from app.models.order import Order
from app.models.payment import Payment
from app.models.menu import Menu

@app.route('/payment/get_all_payment')
def payment_list():
    db_payment = Payment.query.all()
    payments = list(map(lambda x: x.to_dict(), db_payment))
    payments.sort(key=(lambda x: x['payment_id']))
    return jsonify(payments)


@app.route('/payment/create', methods=('GET', 'POST'))
def payment_create():
    app.logger.debug("Payment - CREATE")
    if request.method == 'POST':
        
        result = request.form.to_dict()

        validated = True
        valid_keys = ['payment_method', 'payment_time', 'amount']
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
                table = Tables.query.get(table_id)
                table.update_status('Available')
                
                db.session.commit()
                
            except Exception as ex:
                app.logger.error(f"Error create new order: {ex}")
                raise
            
    return payment_list()

@app.route('/payment/update', methods=('GET', 'POST'))
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
def payment_delete():
    app.logger.debug("Payment - DELETE")
    if request.method == 'POST':
        
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
                db.session.delete(payment)
                db.session.commit()
                
            except Exception as ex:
                app.logger.error(f"Error create new order: {ex}")
                raise
            
    return payment_list()

@app.route('/payment/create_slip', methods=('GET', 'POST'))
def slip_create():
    app.logger.debug("Payment - CREATE SLIP")
    if request.method == 'POST':
        result = request.form.to_dict()
        table_id = result.get('table_id', '')
        app.logger.debug(table_id)
        db_order = db.session.query(Order).filter(Order.table_id == table_id).all() 
        orders = list(map(lambda x: x.to_dict(), db_order))
        menu_list = dict()
        sum_list = dict()
        subtotal = 0
        for order in orders:
            subtotal += order['total_price']
            menu_list = merge_dict(menu_list, order['menu_list'])

        for menu_id in menu_list:
            menu = get_menu_dict(menu_id)
            sum_list[menu['name']] = {'price' : menu_list[menu_id] * menu['price'],
                                      'price_per_unit': menu['price'],
                                      'amount': menu_list[menu_id]}
    
        total = subtotal * 7 / 100
        temp = {'vat_7%': total, 'total' : subtotal, 'sum_price': sum_list}
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