from app import db
from sqlalchemy_serializer import SerializerMixin
# import qrcode



class Tables(db.Model, SerializerMixin):
    __tablename__ = "Tables"

    # table_id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, primary_key=True)
    # qrcode = db.Column(db.LargeBinary, nullable=True)  # for qrcode image
    qrcode = db.Column(db.String(100))
    status = db.Column(db.String(20), nullable=False, default="Available")  # สถานะโต๊ะ

    '''
    สถานะโต๊ะ ("Available", "Occupied", "Reserved", "Paid")
    '''

    def __init__(self, table_id, qrcode):
        self.table_id = table_id
        self.qrcode = qrcode 
        self.status = "Available"

    def update(self, table_id, qrcode, status):
        self.qrcode = qrcode
        self.status = status
        self.table_id = table_id

    def update_status(self, status):
        self.status = status
