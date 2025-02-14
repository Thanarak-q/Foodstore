# Model สำหรับตารางข้อมูลพนักงาน
from app import db
from sqlalchemy_serializer import SerializerMixin
# from flask_login import UserMixin

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
