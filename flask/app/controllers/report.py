import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from app import app
from datetime import datetime, timedelta
from flask_login import login_required
from app.controllers.role_controller import roles_required
from app.models.payment import Payment
from app import db

@app.route('/report')
@login_required
@roles_required('Admin')
def report():
    return render_template('Admin_page/report.html')


def get_customers_by_period(start_date=None):
    query = db.session.query(Payment.payment_time, Payment.payment_id)
    
    if start_date:
        query = query.filter(Payment.payment_time >= start_date)
    
    results = query.all()
    
    day_counts = {"Sunday": 0, "Monday": 0, "Tuesday": 0, "Wednesday": 0,
                  "Thursday": 0, "Friday": 0, "Saturday": 0}
    
    for payment_time, _ in results:
        weekday = payment_time.strftime('%A') 
        day_counts[weekday] += 1
    
    return day_counts

@app.route('/weekly_customers')
def get_weekly_customers():
    now = datetime.utcnow()
    start_date = now - timedelta(days=now.weekday()) 
    return jsonify(get_customers_by_period(start_date))

@app.route('/monthly_customers')
def get_monthly_customers():
    now = datetime.utcnow()
    start_date = now.replace(day=1) 
    return jsonify(get_customers_by_period(start_date))

@app.route('/yearly_customers')
def get_yearly_customers():
    now = datetime.utcnow()
    start_date = now.replace(month=1, day=1) 
    return jsonify(get_customers_by_period(start_date))

@app.route('/all_time_customers')
def get_all_time_customers():
    return jsonify(get_customers_by_period())