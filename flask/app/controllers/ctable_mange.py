# import json
# from flask import (jsonify, render_template,
#                   request, url_for, flash, redirect)
# import qrcode
# from sqlalchemy.sql import text
# from app import app
# from app import db

# from app.controllers import Admin
# from app.models.base import CTable

# @app.route('/table', methods=('GET', 'POST'))
# def table_lists():
#     if request.method == 'POST':
#         result = request.form.to_dict()
#         app.logger.debug(str(result))
#         id_ = result.get('id', '')  # รับค่า id จากฟอร์ม
#         validated = True
#         validated_dict = dict()
#         valid_keys = ['ctable_name', 'qr_code', 'status']

#         # Validate the input
#         for key in result:
#             if key not in valid_keys:
#                 continue

#             value = result[key].strip()
#             if not value or value == 'undefined':
#                 validated = False
#                 break
#             validated_dict[key] = value

#         if validated:
#             app.logger.debug('Validated dict: ' + str(validated_dict))
#             if not id_:  # ถ้าไม่มี id => เพิ่มใหม่
#                 entry = CTable(**validated_dict)
#                 db.session.add(entry)
#             else:  # ถ้ามี id => แก้ไขรายการเดิม
#                 table = CTable.query.filter_by(cTable_name=id_).first()
#                 if table:
#                     for key, value in validated_dict.items():
#                         setattr(table, key, value)

#             db.session.commit()

#         return table_db_tables()
#     return render_template('Admin_page/list_table.html')



# @app.route("/table/tables")
# def table_db_tables():
#     tables = []
#     # ดึงข้อมูลจากฐานข้อมูล พร้อมเรียงลำดับตาม ctable_name
#     db_tables = CTable.query.order_by(CTable.ctable_name).all()  # Use ctable_name instead of cTable_name

#     tables = list(map(lambda x: x.to_dict(), db_tables))
#     app.logger.debug("DB Tables (Sorted): " + str(tables))

#     return jsonify(tables)



# @app.route('/table/remove_table', methods=('GET', 'POST'))
# def table_remove_table():
#     app.logger.debug("table - REMOVE TABLE")
#     if request.method == 'POST':
#         result = request.form.to_dict()
#         id_ = result.get('id', '')
#         try:
#             table = CTable.query.get(id_)
#             db.session.delete(table)
#             db.session.commit()
#         except Exception as ex:
#             app.logger.error(f"Error removing table with id {id_}: {ex}")
#             raise
#     return table_db_tables()

# @app.route('/table/create_table', methods=('GET', 'POST'))
# def table_create_table():
#     app.logger.debug("table - CREATE TABLE")
#     if request.method == 'POST':
#         result = request.form.to_dict()

#         validated = True
#         validated_dict = dict()
#         valid_keys = ['ctable_name', 'status']
#         for key in result:
#             app.logger.debug(f"{key}: {result[key]}")
#             # screen of unrelated inputs
#             if key not in valid_keys:
#                 continue

#             value = result[key].strip()
#             if not value or value == 'undefined':
#                 validated = False
#                 break
#             validated_dict[key] = value

#         validated_dict['qr_code'] = gennerate_qrcode(validated_dict['ctable_name'])
#         if validated:
#             try:
#                 db.session.add(CTable(**validated_dict))
#                 db.session.commit()
#             except Exception as ex:
#                 app.logger.error(f"Error creating table with id {validated_dict['ctable_name']}: {ex}")
#                 raise    

#     return table_db_tables()
        

# def gennerate_qrcode(id):
#     img = qrcode.make('google.com') # Must to change to menu select url
#     type(img)  # qrcode.image.pil.PilImage
#     img.save(f"static/qrcode/{id}.png")
#     return f"static/qrcode/{id}.png"