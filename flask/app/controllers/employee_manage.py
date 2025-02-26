import json
from sqlalchemy.sql import text
from app import app
from app import db
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user

from app.controllers import Admin
from app.models.employee import Employee

@app.route('/em', methods=('GET', 'POST'))
@login_required
def em_list():
    if request.method == 'POST':
        if current_user.role != 'Admin':
            return 'You are not Admin'
        
        result = request.form.to_dict()
        app.logger.debug(str(result))
        id_ = result.get('id', '')  # รับค่า id จากฟอร์ม
        validated = True
        validated_dict = dict()
        valid_keys = ['username', 'password', 'firstname', 'lastname', 'phone', 'role']

        # Validate the input
        for key in result:
            if key not in valid_keys:
                continue

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value
        
        user = Employee.query.filter_by(username=validated_dict['username']).with_for_update().first()
 
        if user:
            flash('username address already exists')
            # if the user doesn't exist or password is wrong, reload the page
            return render_template('Admin_page/login.html')
        
        validated_dict['password'] = generate_password_hash(validated_dict['password'],method='sha256')


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
@login_required
def em_remove_em():    
    if request.method == 'POST':
        if current_user.role != 'Admin':
            return 'You are not Admin'
        app.logger.debug("em - REMOVE em")
        result = request.form.to_dict()
        id_ = result.get('id', '')
        try:
            em = Employee.query.get(id_)
            db.session.delete(em)
            db.session.commit()
        except Exception as ex:
            app.logger.error(f"Error removing em with id {id_}: {ex}")
            raise
    return em_db_ems()

