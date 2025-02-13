from app import db
from sqlalchemy_serializer import SerializerMixin
import datetime
# '''
# การตั้งชื่อ ไฟล์ ตัวเล็ก 
# คลาส ตัวแรกเป็นตัวใหญ่ที่เหลือเล็ก
# ชื่อ table ตัวเล็ก
# ชื่อ attribute ตัวเล็ก

# primary_key=True = ข้อมูลในคอลัมนั้นต้องไม่ซ้ำกัน
# nullable=False = ข้อมูลในคอลัมนั้นต้องไม่ว่างเปล่า
# '''

# # Model สำหรับตารางข้อมูลคำสั่งซื้อ
class Order(db.Model, SerializerMixin):
    __tablename__ = "orders"

    order_id = db.Column(db.Integer, primary_key=True)  # รหัสคำสั่งซื้อ (Primary Key)
    table_name = db.Column(db.Integer, db.ForeignKey('tables.table_name'), nullable=False)  # รหัสโต๊ะที่สั่ง (Foreign Key)
    order_time = db.Column(db.DateTime, nullable=False)  # เวลาที่สั่ง
    status = db.Column(db.String(20), nullable=False, default="Preparing")  # สถานะคำสั่งซื้อ
    '''
    สถานะคำสั่งซื้อ (Preparing, Ready, Served, Paid)
    '''
    total_price = db.Column(db.Float, nullable=False, default=0.0)  # ยอดรวมคำสั่งซื้อ

    def __init__(self, table_name, status="Preparing", total_price=0.0):
        self.table_name = table_name
        self.order_time = datetime.datetime.now()
        self.status = status
        self.total_price = total_price

    def update(self, status, total_price):
        self.status = status
        self.total_price = total_price


# # Model สำหรับตารางรายละเอียดคำสั่งซื้อ
# class OrderDetail(db.Model, SerializerMixin):
#     __tablename__ = "order_details"

#     order_detail_id = db.Column(db.Integer, primary_key=True)  # รหัสรายการคำสั่งซื้อ (Primary Key)
#     order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)  # รหัสคำสั่งซื้อ (Foreign Key)
#     menu_id = db.Column(db.Integer, db.ForeignKey('menu.menu_id'), nullable=False)  # รหัสเมนูที่สั่ง (Foreign Key)
#     quantity = db.Column(db.Integer, nullable=False)  # จำนวนที่สั่ง
#     price_per_unit = db.Column(db.Float, nullable=False)  # ราคาต่อหน่วย
#     total_price = db.Column(db.Float, nullable=False)  # ราคารวมของรายการนี้

#     def __init__(self, order_id, menu_id, quantity, price_per_unit):
#         self.order_id = order_id
#         self.menu_id = menu_id
#         self.quantity = quantity
#         self.price_per_unit = price_per_unit
#         self.total_price = quantity * price_per_unit

#     def update(self, quantity, price_per_unit):
#         self.quantity = quantity
#         self.price_per_unit = price_per_unit
#         self.total_price = quantity * price_per_unit
