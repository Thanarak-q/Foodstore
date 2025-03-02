from app import db
from sqlalchemy_serializer import SerializerMixin

class Store(db.Model, SerializerMixin):
    __tablename__ = 'store'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    vat = db.Column(db.Float)
    service_charge = db.Column(db.Float) 
    Max_Menu_per_Round = db.Column(db.Integer)
    Max_Food_Quantity_per_Order = db.Column(db.Integer)
    Tax = db.Column(db.String(100))
    Promptpay_id = db.Column(db.String(13))

    def __init__(self, name, vat, service_charge, Max_Menu_per_Round, Max_Food_Quantity_per_Order, Tax, Promptpay_id):
        self.name = name
        self.vat = vat
        self.service_charge = service_charge
        self.Max_Menu_per_Round = Max_Menu_per_Round
        self.Max_Food_Quantity_per_Order = Max_Food_Quantity_per_Order
        self.Tax = Tax
        self.Promptpay_id = Promptpay_id

    def update_name(self, name):
        self.name = name
        db.session.commit()

    def update_vat(self, vat):
        self.vat = vat
        db.session.commit()

    def update_max_menu(self, Max_Menu_per_Round):
        self.Max_Menu_per_Round = Max_Menu_per_Round
        db.session.commit()

    def update_max_food(self, Max_Food_Quantity_per_Order):
        self.Max_Food_Quantity_per_Order = Max_Food_Quantity_per_Order
        db.session.commit()

    def update_service_charge(self, service_charge):
        self.service_charge = service_charge
        db.session.commit()

    def update_service_charge(self, service_charge):
        self.service_charge = service_charge
        db.session.commit()
        
    def update_tax(self, Tax):
        self.Tax = Tax
        db.session.commit()

    def update_promptpay(self, promptpay):
        self.Promptpay_id = promptpay
        db.session.commit()
    