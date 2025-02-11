from app import db
from sqlalchemy_serializer import SerializerMixin
# import qrcode

'''
การตั้งชื่อ ไฟล์ ตัวเล็ก 
คลาส เป็นตัวใหญ่ 
ชื่อ cTable ตัวเล็ก
ชื่อ attribute ตัวเล็ก

primary_key=True = ข้อมูลในคอลัมนั้นต้องไม่ซ้ำกัน
nullable=False = ข้อมูลในคอลัมนั้นต้องไม่ว่างเปล่า
'''

# Model สำหรับตารางข้อมูลโต๊ะอาหาร
class CTable(db.Model, SerializerMixin):
    __tablename__ = "cTables"

    CT_id = db.Column(db.Integer, primary_key=True)  # เพิ่มคอลัมน์ id
    qr_code = db.Column(db.String(255), nullable=True)  # ลิงก์ QR Code สำหรับโต๊ะ
    status = db.Column(db.String(20), nullable=False, default="Available")  # สถานะโต๊ะ

    '''
    สถานะโต๊ะ ("Available", "Occupied", "Reserved")
    '''

    def __init__(self, qr_code=None, status="Available"):
        self.qr_code = qr_code or "let me love you like a woman"
        self.status = status

    def update(self, qr_code, status):
        self.qr_code = qr_code
        self.status = status


class Menu(db.Model, SerializerMixin):
    __tablename__ = "menu"

    menu_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    availability = db.Column(db.Boolean, nullable=False)  # เปลี่ยนเป็น Boolean

    def __init__(self, name, description, price, category, image_url=None, availability=True):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.image_url = image_url
        self.availability = availability


    def update(self, name, description, price, category, image_url, availability):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.image_url = image_url
        self.availability = availability


# Model สำหรับตารางข้อมูลพนักงาน
class Employee(db.Model, SerializerMixin):
    __tablename__ = "employee"

    em_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __init__(self, firstname, lastname, phone, role):
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.role = role

    def update(self, firstname, lastname, phone, role):
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.role = role

