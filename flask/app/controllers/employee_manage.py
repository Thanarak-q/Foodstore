import json
from sqlalchemy.sql import text
from app import app
from app import db
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user
from app.controllers.role_controller import roles_required 
from app.controllers import Admin
from app.models.employee import Employee
from app.models.noti import Noti

@app.route('/em', methods=('GET', 'POST'))
@login_required
@roles_required('Admin')
def em_list():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
        id_ = result.get('id', '')  # รับค่า id จากฟอร์ม
        validated = True
        validated_dict = dict()
        valid_keys = ['username', 'password', 'firstname', 'lastname', 'phone', 'role']
        print("ผ่าน valid_keys = ['username', 'password', 'firstname', 'lastname', 'phone', 'role']")

        # Validate the input
        for key in result:
            if key not in valid_keys:
                continue
            print(result[key])
            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value
        
        if 'username' not in validated_dict:
            flash('Username is required')
            return render_template('Admin_page/list_em.html')

        user = Employee.query.filter_by(username=validated_dict['username']).with_for_update().first()
        validated_dict['password'] = generate_password_hash(validated_dict['password'], method='sha256')
        # print(validated_dict['password'])
        
        if validated:
            app.logger.debug('Validated dict: ' + str(validated_dict))
            
            if not id_:  # ถ้าไม่มี id => เพิ่มใหม่
                print("ไม่ผ่าน เช็คซ้ำ")
                entry = Employee(**validated_dict)
                db.session.add(entry)
                last_employee = Employee.query.order_by(Employee.id.desc()).first()
                last_employee_id = last_employee.id if last_employee else 0
                next_employee_id = last_employee_id
                newNoti = Noti(                    
                    type="Employee",
                    message="มีการสร้างพนักงงานใหม่ ไอดีที่" + str(next_employee_id),
                    link='http://localhost:56733/em'
                )
                db.session.add(newNoti)
                db.session.commit()

            else:  # ถ้ามี id => แก้ไขรายการเดิม
                print("ผ่าน เช็คซ้ำ")
                employee = Employee.query.get(id_)
                if employee:
                    for key, value in validated_dict.items():
                        setattr(employee, key, value)
                
                newNoti = Noti(                    
                    type="Employee",
                    message="มีการแก้ไขข้อมูลพนักงาน ไอดีที่" + str(id_),
                    link='http://localhost:56733/em'
                )
                db.session.add(newNoti)
                db.session.commit()

            db.session.commit()

        return em_db_ems()
    return render_template('Admin_page/list_em.html')

@app.route("/em/get_all_em")
def em_db_ems():
    ems = []
    # ดึงข้อมูลจากฐานข้อมูล พร้อมเรียงลำดับตาม name
    db_employees = Employee.query.all()
    ems = list(map(lambda x: x.to_dict(), db_employees))
    app.logger.debug("DB employees (Sorted): " + str(ems))
    return jsonify(ems)

@app.route('/em/remove_em', methods=('GET', 'POST'))
@login_required
@roles_required('Admin')
def em_remove_em():    
    if request.method == 'POST':
        app.logger.debug("em - REMOVE em")
        result = request.form.to_dict()
        id_ = result.get('id', '')
        try:
            em = Employee.query.get(id_)
            em.change_status('Disable')
            db.session.commit()

            newNoti = Noti(                    
                type="Employee",
                message="ลบพนักงงาน ไอดีที่" + str(id_),
                link='http://localhost:56733/em'
            )
            db.session.add(newNoti)
            db.session.commit()
        except Exception as ex:
            app.logger.error(f"Error removing em with id {id_}: {ex}")
            raise
    return em_db_ems()

