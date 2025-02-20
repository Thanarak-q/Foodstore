from app import db
from sqlalchemy_serializer import SerializerMixin
import random

class Menu(db.Model, SerializerMixin):
    __tablename__ = "menu"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    availability = db.Column(db.Boolean, nullable=False)
    ordered = db.Column(db.Integer)

    def __init__(self, name, description, price, category, image_url=None, availability=True):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.image_url = image_url
        self.availability = availability
        self.ordered = random.randint(0, 200)


    def update(self, name, description, price, category, image_url, availability):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.image_url = image_url
        self.availability = availability

    def update_availability(self, availability):
        self.availability = availability

    def update_ordered(self, plus):
        self.ordered += plus