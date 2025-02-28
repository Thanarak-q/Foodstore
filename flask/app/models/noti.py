from app import db
from sqlalchemy_serializer import SerializerMixin

class Noti(db.Model, SerializerMixin):
    __tablename__ = "noti"

    notification_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    is_read = db.Column(db.Boolean, default=False)
    related_id = db.Column(db.Integer)

    def __init__(self, type, message, link=None, related_id=None):
        self.type = type
        self.message = message
        self.link = link
        self.related_id = related_id

    def update(self, type=None, message=None, link=None, related_id=None, is_read=None):
        if type is not None:
            self.type = type
        if message is not None:
            self.message = message
        if link is not None:
            self.link = link
        if related_id is not None:
            self.related_id = related_id
        if is_read is not None:
            self.is_read = is_read

    def mark_as_read(self):
        self.is_read = True

    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "type": self.type,
            "message": self.message,
            "link": self.link,
            "created_at": self.created_at.isoformat(),
            "is_read": self.is_read,
            "related_id": self.related_id
        }