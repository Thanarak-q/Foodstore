import json
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)

import qrcode
from sqlalchemy.sql import text
from app import app
from app import db

from app.controllers import Admin
from app.models.table import Tables

@app.route('/table/get_all_table')
def table_list():
    db_allTable = Tables.query.all()
    tables = list(map(lambda x: x.to_dict(), db_allTable))
    tables.sort(key=(lambda x: int(x['table_id'])))
    app.logger.debug(f"DB Get tables data: {tables}")
    return jsonify(tables)

@app.route('/table/create', methods=('GET', 'POST'))
def table_create():
    app.logger.debug("Tables - CREATE")
    if request.method == 'POST':
        
        result = request.form.to_dict()

        validated = True
        valid_keys = ['is_employee']
        for key in result:
            app.logger.debug(f"{key}: {result[key]}")
            # screen of unrelated inputs
            if key not in valid_keys:
                continue


            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            if key == 'is_employee' and result[key].lower() != "true":
                validated = False    
                break
            
        if validated:
            try:
                db_allTable = Tables.query.all()
                tables = list(map(lambda x: x.to_dict(), db_allTable))
                id = len(tables) + 1
                qrCode = gennerate_qrcode(id)
                db.session.add(Tables(table_id=id, qrcode=qrCode))
                db.session.commit()
                
            except Exception as ex:
                app.logger.error(f"Error create new table: {ex}")
                raise
            
    return table_list()

def gennerate_qrcode(id):
    img = qrcode.make('google.com') # Must to change to menu select url
    type(img)  # qrcode.image.pil.PilImage
    img.save(f"app/static/qrcode/{id}.png")
    return f"app/static/qrcode/{id}.png"

@app.route('/table/update', methods=('GET', 'POST'))
def table_update():
    if request.method == 'POST':
        app.logger.debug("Tables - UPDATE")
        result = request.form.to_dict()
        
        validated = True
        validated_dict = dict()
        valid_keys = ['is_employee', 'table_id', 'status']
        is_employee = result.get('is_employee', '')

        for key in result:
            app.logger.debug(f"{key}: {result[key]}")
            # screen of unrelated inputs
            if key not in valid_keys is True:
                continue
            

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            if key == 'is_employee' and result[key].lower() != "true":
                validated = False    
                break
            validated_dict[key] = value

        app.logger.debug(validated_dict)
        if validated:
            try:
                table = Tables.query.get(validated_dict['table_id'])
                table.update_status(validated_dict['status'])
                db.session.commit()
            except Exception as ex:
                app.logger.error(f"Error update status: {ex}")
                raise

    return table_list()

@app.route('/table/delete', methods=('GET', 'POST'))
def table_delete():
    if request.method == 'POST':
        app.logger.debug("Tables - DELETE")
        result = request.form.to_dict()

        validated = True
        validated_dict = dict()
        valid_keys = ['is_employee', 'table_id']
        for key in result:
            app.logger.debug(f"{key}: {result[key]}")
            # screen of unrelated inputs
            if key not in valid_keys:
                continue


            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            if key == 'is_employee' and result[key].lower() != "true":
                validated = False    
                break
            validated_dict[key] = value
            
        if validated:
            try:
                table = Tables.query.get(validated_dict['table_id'])
                db.session.delete(table)
                db.session.commit()
            except Exception as ex:
                app.logger.error(f"Error delete: {ex}")
                raise

    return table_list()