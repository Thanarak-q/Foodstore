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
    count = db.Column(db.Integer, nullable=False)
    

    '''
    สถานะโต๊ะ ("Available","Occupied", "Reserved", "Paid", "Disable")
    '''

    def __init__(self, qrcode):
        self.qrcode = qrcode
        self.count = 0
        self.status = "Available"

    def update_status(self, status):
        self.status = status
        if status == "Available":
            self.count += 1

    def change_qrcode(self, qrcode):
        self.qrcode_url = qrcode

    # def gennerate_qrcode(self, id):
    #     img = qrcode.make('google.com') # Must to change to menu select url
    #     type(img)  # qrcode.image.pil.PilImage
    #     img.save(f"app/static/qrcode/{id}.png")
    #     return f"app/static/qrcode/{id}.png"
