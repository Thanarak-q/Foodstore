import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app import app
from werkzeug.utils import secure_filename
from app.models.store import Store
from app.controllers.role_controller import roles_required
from app.models.noti import Noti
from app import db


# Define the paths for sounds and logos
SOUNDS_FOLDER = os.path.join(app.static_folder, 'sounds')
LOGO_FOLDER = os.path.join(app.static_folder, 'ico')

# Ensure the directories exist
os.makedirs(SOUNDS_FOLDER, exist_ok=True)
os.makedirs(LOGO_FOLDER, exist_ok=True)

@app.route('/setting', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def setting():
    if request.method == 'POST':
        response_data = {'success': False, 'message': ''}

        try:
            # Handle file uploads
            if 'cooking_sound' in request.files:
                cooking_sound = request.files['cooking_sound']
                if cooking_sound.filename != '':
                    filename = "cooking_room.mp3"
                    cooking_sound.save(os.path.join(SOUNDS_FOLDER, filename))
                    response_data['message'] = 'อัปโหลดเสียงห้องครัวสำเร็จ'
                    response_data['success'] = True

                    newNoti = Noti(                    
                        type="Setting",
                        message="มีการแก้ไขเสียงแจ้งเตือนห้องครัว",
                        link='http://localhost:56733/setting'
                    )
                    db.session.add(newNoti)
                    db.session.commit()

            if 'waiter_sound' in request.files:
                waiter_sound = request.files['waiter_sound']
                if waiter_sound.filename != '':
                    filename = "waiter.mp3"
                    waiter_sound.save(os.path.join(SOUNDS_FOLDER, filename))
                    response_data['message'] = 'อัปโหลดเสียงพนักงานเสิร์ฟสำเร็จ'
                    response_data['success'] = True

                    newNoti = Noti(                    
                        type="Setting",
                        message="มีการแก้ไขเสียงแจ้งเตือนพนักงานเสริฟ",
                        link='http://localhost:56733/setting'
                    )
                    db.session.add(newNoti)
                    db.session.commit()

            if 'logo_file' in request.files:
                logo_file = request.files['logo_file']
                if logo_file.filename != '':
                    filename = "logo.jpg"
                    logo_file.save(os.path.join(LOGO_FOLDER, filename))
                    response_data['message'] = 'อัปโหลดโลโก้สำเร็จ'
                    response_data['success'] = True

                    newNoti = Noti(                    
                        type="Setting",
                        message="มีการแก้ไขโลโก้ร้าน",
                        link='http://localhost:56733/setting'
                    )
                    db.session.add(newNoti)
                    db.session.commit()

            # Handle form data
            store = Store.query.first()
            if store:
                if 'name' in request.form:
                    name = request.form['name']
                    store.update_name(name)
                    response_data['message'] = 'อัปเดตชื่อร้านสำเร็จ'
                    response_data['success'] = True

                    newNoti = Noti(                    
                        type="Setting",
                        message="มีการแก้ไขชื่อร้าน",
                        link='http://localhost:56733/setting'
                    )
                    db.session.add(newNoti)
                    db.session.commit()

                if 'vat_rate' in request.form:
                    vat_rate = float(request.form['vat_rate'])
                    store.update_vat(vat_rate)
                    response_data['message'] = 'อัปเดต VAT สำเร็จ'
                    response_data['success'] = True

                    newNoti = Noti(                    
                        type="Setting",
                        message="มีการแก้ไข vat",
                        link='http://localhost:56733/setting'
                    )
                    db.session.add(newNoti)
                    db.session.commit()

                if 'service_charge' in request.form:
                    service_charge = float(request.form['service_charge'])
                    store.update_service_charge(service_charge)
                    response_data['message'] = 'อัปเดตค่าบริการสำเร็จ'
                    response_data['success'] = True

                    newNoti = Noti(                    
                        type="Setting",
                        message="มีการแก้ไข service charge",
                        link='http://localhost:56733/setting'
                    )
                    db.session.add(newNoti)
                    db.session.commit()

                if 'max_menu' in request.form:
                    max_orders = int(request.form['max_menu'])
                    store.update_max_menu(max_orders)
                    response_data['message'] = 'อัปเดตจำนวนเมนูต่อออเดอร์สำเร็จ'
                    response_data['success'] = True

                    newNoti = Noti(                    
                        type="Setting",
                        message="มีการแก้ไขจำนวนเมนูต่อออเดอร์",
                        link='http://localhost:56733/setting'
                    )
                    db.session.add(newNoti)
                    db.session.commit()

                if 'max_food_quantity' in request.form:
                    max_food_quantity = int(request.form['max_food_quantity'])
                    store.update_max_food(max_food_quantity)
                    response_data['message'] = 'อัปเดตจำนวนอาหารต่อเมนูสำเร็จ'
                    response_data['success'] = True

                    newNoti = Noti(                    
                        type="Setting",
                        message="มีการแก้ไขจำนวนอาหารต่อเมนู",
                        link='http://localhost:56733/setting'
                    )
                    db.session.add(newNoti)
                    db.session.commit()

                if 'Tax_id' in request.form:
                    Tax_id = str(request.form['Tax_id'])
                    store.update_tax(Tax_id)
                    response_data['message'] = 'อัปเดตรหัสผู้เสียภาษีสำเร็จ'
                    response_data['success'] = True

                    newNoti = Noti(                    
                        type="Setting",
                        message="มีการแก้ไขหมายเลขประจำตัวผู้เสียภาษี",
                        link='http://localhost:56733/setting'
                    )
                    db.session.add(newNoti)
                    db.session.commit()
                    
                if 'Promptpay_name' in request.form:
                    Promptpay_name = str(request.form['Promptpay_name'])
                    store.update_promptpayname(Promptpay_name)
                    response_data['message'] = 'อัปเดตชื่อพร้อมเพลย์'
                    response_data['success'] = True

                    newNoti = Noti(                    
                        type="Setting",
                        message="มีการแก้ไขชื่อพร้อมเพลย์",
                        link='http://localhost:56733/setting'
                    )
                    db.session.add(newNoti)
                    db.session.commit()

                if 'Promptpay_id' in request.form:
                    promptpay = str(request.form['Promptpay_id'])
                    temp = is_Prompt_format(promptpay)
                    if temp == 'Wrong Format':
                        response_data['message'] = 'เกิดข้อผิดพลาด: Prompt Pay ผิด'
                        response_data['success'] = False
                    else:
                        store.update_promptpay(promptpay)
                        response_data['message'] = 'อัปเดตรหัสพร้อมเพลย์'
                        response_data['success'] = True

                        newNoti = Noti(                    
                            type="Setting",
                            message="มีการแก้ไขรหัสพร้อมเพลย์",
                            link='http://localhost:56733/setting'
                        )
                        db.session.add(newNoti)
                        db.session.commit()
                    

        except Exception as e:
            response_data['message'] = f'เกิดข้อผิดพลาด: {str(e)}'
            response_data['success'] = False

        return jsonify(response_data)  # ส่งกลับข้อมูลเป็น JSON

    # สำหรับ GET request
    store = Store.query.first()
    return render_template('Admin_page/setting.html', store=store)

def is_Prompt_format(num):
    num = str(num)
    if len(num) != 10 and len(num) != 13 or not num.isdigit():
        return 'Wrong Format'
    return num


@app.route("/store_list")
def store_list():
    store = []
    db_store = Store.query.all()
    store = list(map(lambda x: x.to_dict(), db_store))
    app.logger.debug("DB store (Sorted): " + str(store))
    return jsonify(store)