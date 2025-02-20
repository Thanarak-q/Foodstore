import json
from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)

from app import app
from app import db
from sqlalchemy.sql import text
import datetime

from app.models.table import Tables
from app.models.order import Order
from app.models.payment import Payment

@app.route('/payment/get_all_payment')
def payment_list():
    db_payment = Payment.query.all()
    payments = list(map(lambda x: x.to_dict(), db_payment))
    payments.sort(key=(lambda x: x['payment_id']))
    return jsonify(payments)