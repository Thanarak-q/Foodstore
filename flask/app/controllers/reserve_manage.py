from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)

from app import app
from app import db
from app.models.reserve import Reserve
from app.models.noti import Noti
from flask_login import login_required
from app.controllers.role_controller import roles_required 


@app.route('/reserve/get_all_reserve')
def reserve_list():
    db_allreview = db.session.query(Reserve).filter(Reserve.status == 'Enable').all()
    reserve = list(map(lambda x: x.to_dict(), db_allreview))
    reserve.sort(key=(lambda x: int(x['reserve_id'])))
    return jsonify(reserve)

@app.route('/reserve/create', methods=('GET', 'POST'))
@login_required
@roles_required('Admin', 'Cashier')
def reserve_create():
    
    if request.method == 'POST':
        app.logger.debug("reserve - CREATE")
        result = request.form.to_dict()
        app.logger.debug(result)
        valid_keys = ['table_id', 'reserve_time', 'customer_name', 'customer_phone_number', 'cashier_id']
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
        validated_dict['phone'] = phonenumber_format(validated_dict['phone'])
        if validated:
            try:
                temp = Reserve(
                    **validated_dict
                )
                db.session.add(temp)
                db.session.commit()
                
                newNoti = Noti(                    
                    type="Reserve",
                    message="จองโต๊ะ",
                    link='http://localhost:56733/orders'
                )
                db.session.add(newNoti)
                db.session.commit()

            except Exception as ex:
                app.logger.error(f"Error create new reserve: {ex}")
                raise
            
    return reserve_list()

@app.route('/reserve/update', methods=('GET', 'POST'))
@login_required
@roles_required('Admin', 'Cashier')
def reserve_update():
    
    if request.method == 'POST':
        
        app.logger.debug("reserve - UPDATE")
        result = request.form.to_dict()
        app.logger.debug(result)
        valid_keys = ['table_id', 'reserve_time', 'customer_name', 'customer_phone_number', 'cashier_id']
        reserve_id = result.get('reserve_id', '')
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
        validated_dict['phone'] = phonenumber_format(validated_dict['phone'])
        if validated:
            try:
                reserve = Reserve.query.get(reserve_id)
                reserve.update(**validated_dict)
                
                db.session.commit()
                
            except Exception as ex:
                app.logger.error(f"Error create new review: {ex}")
                raise
            
    return reserve_list()

@app.route('/reserve/delete', methods=('GET', 'POST'))
@login_required
@roles_required('Admin')
def reserve_delete():
    
    if request.method == 'POST':
        
        app.logger.debug("reserve - DELETE")
        result = request.form.to_dict()
        app.logger.debug(result)
        valid_keys = ['reserve_id']
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
                reserve = Reserve.query.get(validated_dict['reserve_id'])
                reserve.change_status('Disable')
                
                db.session.commit()
                
            except Exception as ex:
                app.logger.error(f"Error delete new reserve: {ex}")
                raise
            
    return reserve_list()

def phonenumber_format(phonenumber):
    phonenumber = str(phonenumber)
    temp = ''
    for digit in phonenumber:
        if digit.isdigit():
            # print(digit)
            temp += digit
    if len(temp) != 10:
        return 'Wrong Format'
    return temp[:3] + '-' + temp[3:6] + '-' + temp[6:]
