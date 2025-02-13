from app import db
from sqlalchemy_serializer import SerializerMixin

class Menu(db.Model, SerializerMixin):
    __tablename__ = "menu"

    name = db.Column(db.String(100), primary_key=True)
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