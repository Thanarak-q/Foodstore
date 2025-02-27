import json
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)

from app import app
from app import db
from sqlalchemy.sql import text
from flask_login import login_required, current_user
from app.controllers.role_controller import roles_required 
from app.models.order import Order
from app.models.menu import Menu



@app.route('/orders')
def orders():
    return render_template('Admin_page/order_list.html')

@app.route('/orders/get_all_orders')
def orders_list():
    db_allOrder = Order.query.all()
    orders = list(map(lambda x: x.to_dict(), db_allOrder))
    orders.sort(key=(lambda x: int(x['order_id'])))
    return jsonify(orders)

@app.route('/orders/create', methods=('GET', 'POST'))
def order_create():
    app.logger.debug("Order - CREATE")
    if request.method == 'POST':
        
        result = request.form.to_dict()
        app.logger.debug(result)
        valid_keys = ['table_id', 'time']
        validated = True
        validated_dict = dict()
        validated_dict['menu_list'] = dict()
        for key in result:
            app.logger.debug(f"{key}: {result[key]}")
            # screen of unrelated inputs
            if key not in valid_keys:
                validated_dict['menu_list'][key] = int(result[key])
                continue

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break

            validated_dict[key] = value
        app.logger.debug(validated_dict)
        if validated:
            try:
                temp = Order(
                    table_id=int(validated_dict['table_id']),
                    time=validated_dict['time'],
                    status='Preparing',
                    menu_list=validated_dict['menu_list']
                )
                temp.change_price(cal_price(validated_dict['menu_list']))
                db.session.add(temp)
                
                db.session.commit()
                
            except Exception as ex:
                app.logger.error(f"Error create new order: {ex}")
                raise
            
    return orders_list()

@app.route('/orders/admin', methods=('GET', 'POST'))
@login_required
@roles_required('Admin')
def order_admin():
    app.logger.debug("Order - CREATE")
    if request.method == 'POST':
        
        result = request.form.to_dict()
        app.logger.debug(result)
        valid_keys = ['table_id', 'time', 'status']
        id_ = result['order_id']
        validated = True
        validated_dict = dict()
        validated_dict['menu_list'] = dict()
        for key in result:
            app.logger.debug(f"{key}: {result[key]}")
            # screen of unrelated inputs
            if key == 'order_id':
                continue

            if key not in valid_keys:
                validated_dict['menu_list'][key] = int(result[key])
                continue

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break

            validated_dict[key] = value
        app.logger.debug(validated_dict)
        if validated:
            try:
                orders = Order.query.filter_by(order_id=int(id_)).first()
                if orders == None:
                    temp = Order(
                    table_id=int(validated_dict['table_id']),
                    time=validated_dict['time'],
                    status=validated_dict['status'],
                    menu_list=validated_dict['menu_list']
                )
                    temp.change_price(cal_price(validated_dict['menu_list']))
                    db.session.add(temp)
                else:
                    orders.table_id = int(validated_dict['table_id'])
                    orders.time = validated_dict['time']
                    orders.status = validated_dict['status']
                    orders.menu_list = validated_dict['menu_list']
                    orders.change_price(cal_price(validated_dict['menu_list']))
                db.session.commit()
                
            except Exception as ex:
                app.logger.error(f"Error create new order: {ex}")
                raise
            
    return orders_list()

def cal_price(menu_list):
        db_allmenus = Menu.query.all()
        menus = list(map(lambda x: x.to_dict(), db_allmenus))
        menus.sort(key=(lambda x: int(x['id'])))
        app.logger.debug(f"DB Get menus data to cal_price() in Order")

        total = 0
        # note menu_list key start at 0 but menus start at 1
        for key in menu_list:
            app.logger.debug(type(menus[int(key) - 1]['price']))
            app.logger.debug(f"{key} : {int(menus[int(key) - 1]['price']) * menu_list[key]}")
            total += int(menus[int(key) - 1]['price']) * menu_list[key]
            plus_menu_ordered(key, menu_list[key])
            
        return total

def plus_menu_ordered(menu_id, amount):
    menu = Menu.query.get(menu_id)
    menu.update_ordered(amount)
    # db.session.commit()



@app.route('/orders/update', methods=('GET', 'POST'))
@login_required
@roles_required('Admin', 'Chef', 'Waiter')
def order_update():
    if request.method == 'POST':
        app.logger.debug("Order - UPDATE")
        # return 'Who are you?'
        result = request.form.to_dict()

        validated_dict, validated = validate_data(result, ['order_id', 'status'])

        app.logger.debug(validated_dict)
        if validated:
            try:
                orders = Order.query.get(validated_dict['order_id'])
                orders.update_status(validated_dict['status'])
                db.session.commit()
            except Exception as ex:
                app.logger.error(f"Error update order status: {ex}")
                raise

    return orders_list()



@app.route('/orders/delete', methods=('GET', 'POST'))
@login_required
@roles_required('Admin')
def order_delete():
    if request.method == 'POST':
        app.logger.debug("Orders - DELETE")
        result = request.form.to_dict()

        validated_dict, validated = validate_data(result, ['order_id'])
            
        if validated:
            try:
                orders = Order.query.get(validated_dict['order_id'])
                db.session.delete(orders)
                db.session.commit()
            except Exception as ex:
                app.logger.error(f"Error delete orders: {ex}")
                raise

    return orders_list()

def validate_data(result, valid_keys=[]):
    validated = True
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
    return validated_dict, validated