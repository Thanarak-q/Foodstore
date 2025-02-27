# Model สำหรับตารางข้อมูลพนักงาน
from app import db
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

# Model สำหรับตารางข้อมูลพนักงาน
class Employee(db.Model, UserMixin):
    __tablename__ = "employee"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password= db.Column(db.String, nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100))
    phone = db.Column(db.String(12), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    '''
    role : Cashier, Chef, Waiter, Admin
    '''

    def __init__(self, firstname, username, password, phone, role, lastname=None):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.role = role

    def update(self, firstname, username, password, phone, role, lastname=None):
        # print("eieieieeieieieii")
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.role = role

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'phone': self.phone,
            'role': self.role
        }

