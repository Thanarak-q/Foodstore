from app import db
from sqlalchemy_serializer import SerializerMixin

# Model สำหรับตารางข้อมูลการชำระเงิน
class Reserve(db.Model, SerializerMixin):
    __tablename__ = 'reserve'

    reserve_id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey('Tables.table_id'), nullable=False)
    reserve_time = db.Column(db.Datetime, nullable=False)
    customer_name = db.Column(db.String, nullable=False)
    customer_phone_number = db.Column(db.String, nullable=False)
    cashier_id = db.Column(db.Integer, db.ForeignKey('Employee.id'), nullable=False)

    def __init__(self, table_id, reserve_time, customer_name, customer_phone_number, cashier_id):
        self.table_id = table_id
        self.reserve_time = reserve_time
        self.customer_name = customer_name
        self.customer_phone_number = customer_phone_number
        self.cashier_id  = cashier_id