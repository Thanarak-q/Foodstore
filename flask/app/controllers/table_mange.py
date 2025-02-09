import json
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)

from sqlalchemy.sql import text
from app import app
from app import db

from app.controllers import Admin
from app.models.base import CTable

@app.route('/table', methods=('GET', 'POST'))
def table_list():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
        id_ = result.get('id', '')  # รับค่า id จากฟอร์ม
        validated = True
        validated_dict = dict()
        valid_keys = ['ctable_name', 'qr_code', 'status']

        # Validate the input
        for key in result:
            if key not in valid_keys:
                continue

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value

        if validated:
            app.logger.debug('Validated dict: ' + str(validated_dict))
            if not id_:  # ถ้าไม่มี id => เพิ่มใหม่
                entry = CTable(**validated_dict)
                db.session.add(entry)
            else:  # ถ้ามี id => แก้ไขรายการเดิม
                table = CTable.query.filter_by(cTable_name=id_).first()
                if table:
                    for key, value in validated_dict.items():
                        setattr(table, key, value)

            db.session.commit()

        return table_db_tables()
    return render_template('Admin_page/list_table.html')



@app.route("/table/tables")
def table_db_tables():
    tables = []
    # ดึงข้อมูลจากฐานข้อมูล พร้อมเรียงลำดับตาม ctable_name
    db_tables = CTable.query.order_by(CTable.ctable_name).all()  # Use ctable_name instead of cTable_name

    tables = list(map(lambda x: x.to_dict(), db_tables))
    app.logger.debug("DB Tables (Sorted): " + str(tables))

    return jsonify(tables)



@app.route('/table/remove_table', methods=('GET', 'POST'))
def table_remove_table():
    app.logger.debug("table - REMOVE TABLE")
    if request.method == 'POST':
        result = request.form.to_dict()
        id_ = result.get('id', '')
        try:
            table = CTable.query.get(id_)
            db.session.delete(table)
            db.session.commit()
        except Exception as ex:
            app.logger.error(f"Error removing table with id {id_}: {ex}")
            raise
    return table_db_tables()