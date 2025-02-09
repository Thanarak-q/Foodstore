import json
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)

from sqlalchemy.sql import text
from app import app
from app import db

from app.controllers import Admin
from app.models.base import Menu

@app.route('/menu', methods=('GET', 'POST'))
def menu_list():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
        id_ = result.get('id', '')  # รับค่า id จากฟอร์ม
        validated = True
        validated_dict = dict()
        valid_keys = ['name', 'description', 'price', 'category', 'image_url', 'availability']

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
            db.session.delete(menu)
            db.session.commit()
        except Exception as ex:
            app.logger.error(f"Error removing menu with id {id_}: {ex}")
            raise
    return menu_db_menus()