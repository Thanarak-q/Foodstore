import json
from sqlalchemy.sql import text
from app import app
from app import db
from app.models.base import Employee
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)

from app.controllers import Admin

@app.route('/em', methods=('GET', 'POST'))
def em_list():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
        id_ = result.get('id', '')  # รับค่า id จากฟอร์ม
        validated = True
        validated_dict = dict()
        valid_keys = ['firstname', 'lastname', 'phone', 'role']

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
                entry = Employee(**validated_dict)
                db.session.add(entry)
            else:  # ถ้ามี id => แก้ไขรายการเดิม
                employee = Employee.query.get(id_)
                if employee:
                    for key, value in validated_dict.items():
                        setattr(employee, key, value)

            db.session.commit()

        return em_db_ems()
    return render_template('Admin_page/list_em.html')

@app.route("/em/ems")
def em_db_ems():
    ems = []
    # ดึงข้อมูลจากฐานข้อมูล พร้อมเรียงลำดับตาม name
    db_employees = Employee.query.all()

    ems = list(map(lambda x: x.to_dict(), db_employees))
    app.logger.debug("DB employees (Sorted): " + str(ems))

    return jsonify(ems)

@app.route('/em/remove_em', methods=('GET', 'POST'))
def em_remove_em():
    app.logger.debug("em - REMOVE em")
    if request.method == 'POST':
        result = request.form.to_dict()
        id_ = result.get('id', '')
        try:
            em = Employee.query.get(id_)
            if em:
                db.session.delete(em)
                db.session.commit()
        except Exception as ex:
            app.logger.error(f"Error removing em with id {id_}: {ex}")
            return jsonify({"status": "error", "message": str(ex)}), 500
    return em_db_ems()