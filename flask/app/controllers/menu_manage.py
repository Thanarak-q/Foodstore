import os
from PIL import Image
from flask import (jsonify, render_template, request, url_for, flash, redirect)
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
import qrcode
from sqlalchemy.sql import text
from app import app, db
from app.models.menu import Menu

UPLOAD_FOLDER = os.path.join(app.static_folder)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/menu', methods=('GET', 'POST'))
@app.route('/menu', methods=('GET', 'POST'))
def menu_list():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
        id_ = result.get('id', '')  # รับค่า id จากฟอร์ม
        validated = True
        validated_dict = dict()
        valid_keys = ['name', 'description', 'price', 'category', 'availability']

        # Validate the input
        for key in result:
            if key not in valid_keys:
                continue

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value

        # แปลงค่า availability จากสตริงเป็นบูลีน
        if 'availability' in validated_dict:
            validated_dict['availability'] = validated_dict['availability'].lower() == 'true'

        # Handle file upload
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and allowed_file(file.filename):
                # เปิดไฟล์ด้วย Pillow
                img = Image.open(file)
                # width, height = 228, 232

                # # คำนวณตำแหน่งของตรงกลางของภาพ
                # img_width, img_height = img.size
                # left = (img_width - width) // 2
                # top = (img_height - height) // 2
                # right = (img_width + width) // 2
                # bottom = (img_height + height) // 2

                # # ตัดรูป
                # img = img.crop((left, top, right, bottom))

                # ทำความสะอาดชื่อไฟล์และกำหนด path
                filename = validated_dict['name'].replace(' ', '_') + '.jpg'
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'food_image', filename)
                
                # ถ้ามี id => แก้ไขรายการเดิม
                if id_:
                    menu = Menu.query.filter_by(name=id_).first()
                    if menu and menu.image_url:
                        # ลบไฟล์ภาพเดิม
                        old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(menu.image_url))
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                
                # บันทึกไฟล์ภาพใหม่หลังจากที่ทำการรีไซส์
                img.save(file_path)
                validated_dict['image_url'] = f'/static/food_image/{filename}'

        if validated:
            app.logger.debug('Validated dict: ' + str(validated_dict))
            if not id_:  # ถ้าไม่มี id => เพิ่มใหม่
                entry = Menu(**validated_dict)
                db.session.add(entry)
            else:  # ถ้ามี id => แก้ไขรายการเดิม
                menu = Menu.query.filter_by(name=id_).first()
                if menu:
                    for key, value in validated_dict.items():
                        setattr(menu, key, value)

            db.session.commit()

        return menu_db_menus()
    return render_template('Admin_page/list_menu.html')

@app.route("/menu/menus")
def menu_db_menus():
    menus = []
    # ดึงข้อมูลจากฐานข้อมูล พร้อมเรียงลำดับตาม name
    db_menus = Menu.query.all()

    menus = list(map(lambda x: x.to_dict(), db_menus))
    menus = menu_get_top3() + menus
    app.logger.debug("DB menus (Sorted): " + str(menus))

    return jsonify(menus)

@app.route('/menu/remove_menu', methods=('GET', 'POST'))
def menu_remove_menu():
    app.logger.debug("menu - REMOVE menu")
    if request.method == 'POST':
        result = request.form.to_dict()
        id_ = result.get('id', '')
        try:
            menu = Menu.query.get(id_)
            if menu.image_url:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(menu.image_url))
                if os.path.exists(image_path):
                    os.remove(image_path)
            db.session.delete(menu)
            db.session.commit()
        except Exception as ex:
            app.logger.error(f"Error removing menu with id {id_}: {ex}")
            raise
    return menu_db_menus()

@app.route('/menus/create', methods=('GET', 'POST'))
def menu_create():
    app.logger.debug("Menu - CREATE")
    if request.method == 'POST':
        
        result = request.form.to_dict()

        validated = True
        valid_keys = ['name', 'description', 'price', 'category', 'image_url', 'availability']
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
                db.session.add(Menu(
                    name = validated_dict['name'],
                    description = validated_dict['description'],
                    price= validated_dict['price'],
                    category= validated_dict['catagory'],
                    image_url= validated_dict['image_url'],
                    availability= validated_dict['availability']
                    ))
                db.session.commit()
                
            except Exception as ex:
                app.logger.error(f"Error create new menu: {ex}")
                raise
            
    return menus_list()

@app.route('/menus/get_all_menus')
def menus_list():
    db_allmenus = Menu.query.all()
    menus = list(map(lambda x: x.to_dict(), db_allmenus))
    menus.sort(key=(lambda x: int(x['id'])))
    app.logger.debug(f"DB Get tables data: {menus}")
    return jsonify(menus)

@app.route('/menus/update', methods=('GET', 'POST'))
def menu_update():
    if request.method == 'POST':
        app.logger.debug("Menu - UPDATE")
        result = request.form.to_dict()
        
        validated = True
        validated_dict = dict()
        valid_keys = ['id', 'availability']

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

        app.logger.debug(validated_dict)
        if validated:
            try:
                menus = Menu.query.get(validated_dict['id'])
                menus.update_availability(validated_dict['availability'])
                db.session.commit()
            except Exception as ex:
                app.logger.error(f"Error update menu availability: {ex}")
                raise

    return menus_list()

@app.route('/menus/delete', methods=('GET', 'POST'))
def menu_delete():
    if request.method == 'POST':
        app.logger.debug("Menu - DELETE")
        result = request.form.to_dict()

        validated = True
        validated_dict = dict()
        valid_keys = ['id']
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
                menus = Menu.query.get(validated_dict['id'])
                db.session.delete(menus)
                db.session.commit()
            except Exception as ex:
                app.logger.error(f"Error delete menu: {ex}")
                raise

    return menus_list()

# @app.route('/menus/top3', methods=('GET', 'POST'))
def menu_get_top3():
    db_allmenus = Menu.query.all()
    menus = list(map(lambda x: x.to_dict(), db_allmenus))
    menus.sort(key=(lambda x: int(x['ordered'])), reverse=True)
    top3 = []
    for i in range(3):
        temp = menus[i]
        temp['category'] = 'เมนูขายดี'
        top3 += [temp]
    return top3

