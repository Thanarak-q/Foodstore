import json
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)

import qrcode
from sqlalchemy.sql import text
from app import app
from app import db
from flask_login import login_required, current_user
import jwt
import datetime
from manage import SECRET_KEY

from app.controllers import Admin
from app.models.table import Tables
from app.models.order import Order
from app.models.noti import Noti
from app.controllers.role_controller import roles_required

@app.route('/table/get_all_table')
def table_list():
    db_allTable = Tables.query.all()
    tables = list(map(lambda x: x.to_dict(), db_allTable))
    tables.sort(key=(lambda x: int(x['table_id'])))
    app.logger.debug(f"DB Get tables data: {tables}")
    return jsonify(tables)

@app.route('/table/create', methods=('GET', 'POST'))
@login_required
@roles_required('Admin')
def table_create():
    if request.method == 'POST':
        app.logger.debug("Tables - CREATE")
        result = request.form.to_dict()

        validated = True
        valid_keys = ['status']
        for key in result:
            app.logger.debug(f"{key}: {result[key]}")
            # screen of unrelated inputs
            if key not in valid_keys:
                continue

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
        if validated:
            try:
                db_allTable = Tables.query.all()
                tables = list(map(lambda x: x.to_dict(), db_allTable))
                tables.sort(key=(lambda x: int(x['table_id'])), reverse=True)
                id = tables[0]['table_id'] + 1
                qrCode = gennerate_qrcode(id, 0)
                db.session.add(Tables(qrcode=qrCode))
                db.session.commit()

                newNoti = Noti(                    
                    type="Table",
                    message="มีการเพิ่มโต๊ะใหม่",
                    link='http://localhost:56733/menu'
                )
                db.session.add(newNoti)
                db.session.commit()
                
            except Exception as ex:
                app.logger.error(f"Error create new table: {ex}")
                raise
            
    return table_list()

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

@app.route('/table/admin', methods=['POST'])
@login_required
@roles_required('Admin')
def table_admin():
    app.logger.debug("table - SUPER FUNC ADMIN")
    if request.method == 'POST':
        
        result = request.form.to_dict()
        app.logger.debug(result)
        valid_keys = ['status']
        id_ = result['table_id']
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
        app.logger.debug(validated_dict)
        if validated:
            try:
                table = Tables.query.filter_by(table_id=int(id_)).first()
                if table == None:
                    db_allTable = Tables.query.all()
                    tables = list(map(lambda x: x.to_dict(), db_allTable))
                    tables.sort(key=(lambda x: int(x['table_id'])), reverse=True)
                    id = tables[0]['table_id'] + 1
                    qrCode = gennerate_qrcode(id, 0)
                    db.session.add(Tables(qrcode=qrCode))
                    db.session.commit()
                    last_menu = Tables.query.order_by(Tables.id.desc()).first()
                    last_menu_id = last_menu.id if last_menu else 0
                    next_menu_id = last_menu_id
                    newNoti = Noti(                
                        type="Table",
                        message="มีการเพิ่มโต๊ะใหม่ ไอดีที่ " + str(next_menu_id),
                        link='http://localhost:56733/menu'
                    )
                    db.session.add(newNoti)

                else:
                    table = Tables.query.get(validated_dict['table_id'])
                    table.update_status(validated_dict['status'])
                    newNoti = Noti(                    
                        type="Table",
                        message="มีการแก้ไขโต๊ะ ไอดีที่ " + str(id_),
                        link='http://localhost:56733/menu'
                    )
                    db.session.add(newNoti)
                    db.session.commit()
                    if validated_dict['status'] == 'Available':
                        table = Tables.query.get(validated_dict['table_id'])
                        qrcode = gennerate_qrcode(table.table_id, table.count)
                        newNoti = Noti(                    
                            type="Order",
                            message="มีการแก้ไขโต๊ะ",
                            link='http://localhost:56733/menu'
                        )
                        db.session.add(newNoti)
                        table.change_qrcode(qrcode)
                db.session.commit()
                
            except Exception as ex:
                app.logger.error(f"Error create new order: {ex}")
                raise
            
    return table_list()

@app.route('/table/update', methods=('GET', 'POST'))
@login_required
@roles_required('Admin', 'Cashier')
def table_update():
    if request.method == 'POST':
        
        app.logger.debug("Tables - UPDATE")
        result = request.form.to_dict()
        
        validated = True
        validated_dict = dict()
        valid_keys = ['table_id', 'status']

        

        for key in result:
            app.logger.debug(f"{key}: {result[key]}")
            # screen of unrelated inputs
            if key not in valid_keys is True:
                continue
            

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value

        if validated_dict['status'] not in ["Available","Occupied", "Reserved", "Disable"]:
            # app.logger.debug(validated_dict['status'])
            validated = False

        # app.logger.debug(validated_dict)
        

        if validated:
            try:
                table = Tables.query.get(validated_dict['table_id'])
                table.update_status(validated_dict['status'])
                newNoti = Noti(                    
                        type="Table",
                        message="มีการแก้ไขโต๊ะ",
                        link='http://localhost:56733/menu'
                )
                db.session.add(newNoti)
                
                if validated_dict['status'] == 'Available':
                    table = Tables.query.get(validated_dict['table_id'])
                    qrcode = gennerate_qrcode(table.table_id, table.count)
                    newNoti = Noti(                    
                        type="Table",
                        message="มีการแก้ไขโต๊ะ ไอดีที่" + str(valid_keys['table_id']),
                        link='http://localhost:56733/menu'
                    )
                    db.session.add(newNoti)
                    table.change_qrcode(qrcode)
                db.session.commit()
            except Exception as ex:
                app.logger.error(f"Error update status: {ex}")
                raise

    return table_list()

@app.route('/table/delete', methods=('GET', 'POST'))
@login_required
@roles_required('Admin')
def table_delete():
    if request.method == 'POST':
        app.logger.debug("Tables - DELETE")
        result = request.form.to_dict()

        validated = True
        validated_dict = dict()
        valid_keys = ['table_id']
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
                table = Tables.query.get(validated_dict['table_id'])
                table.update_status('Disable')
                newNoti = Noti(                    
                    type="Table",
                    message="มีการแก้ไขโต๊ะ",
                    link='http://localhost:56733/menu'
                )
                db.session.add(newNoti)
                db.session.commit()
            except Exception as ex:
                app.logger.error(f"Error delete: {ex}")
                raise

    return table_list()

@app.route('/table/cancel', methods=('POST',))
@login_required
@roles_required('Admin', 'Cashier')
def table_cancle():
    if request.method == 'POST':
        
        app.logger.debug("Tables - CANCEL")
        result = request.form.to_dict()

        validated = True
        validated_dict = dict()
        valid_keys = ['table_id']
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
                table = Tables.query.get(validated_dict['table_id'])
                table.cancle()
                newNoti = Noti(                    
                    type="Table",
                    message="มีการ cancle โต๊ะ",
                    link='http://localhost:56733/menu'
                )
                db.session.add(newNoti)
                db.session.commit()
            except Exception as ex:
                app.logger.error(f"Error cancel: {ex}")
                raise

    return table_list()