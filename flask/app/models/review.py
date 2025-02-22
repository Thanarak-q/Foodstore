from app import db
from sqlalchemy_serializer import SerializerMixin

class Review(db.Model, SerializerMixin):
    __tablename__ = 'review'

    review_id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100))
    review = db.Column(db.String(250))
    star = db.Column(db.Integer)

    def __init__(self, name, review, star):
        self.name = name
        self.review = review
        self.star = star
