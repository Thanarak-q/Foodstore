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
# class CTable(db.Model, SerializerMixin):
#     __tablename__ = "cTables"

#     # table_id = db.Column(db.Integer, primary_key=True)
#     ctable_name = db.Column(db.String(50), primary_key=True)  
#     # qr_code = db.Column(db.LargeBinary, nullable=True)  # for qrcode image
#     qr_code = db.Column(db.String(100), nullable=True)
#     status = db.Column(db.String(20), nullable=False, default="Available")  # สถานะโต๊ะ

#     '''
#     สถานะโต๊ะ ("Available", "Occupied", "Reserved")
#     '''

#     def __init__(self, ctable_name, qr_code=None, status="Available"):
#             self.ctable_name = ctable_name
#             self.qr_code = qr_code or "https://www.youtube.com/watch?v=1Sq0-Y_K2w0"
#             self.status = status

#     def update(self, ctable_name, qr_code, status):
#         self.qr_code = qr_code
#         self.status = status
#         self.ctable_name = ctable_name






