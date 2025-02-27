import os
from flask import Flask, render_template, request, redirect, url_for, flash
from app import app
from flask_login import login_required
from app.controllers.role_controller import roles_required 

@app.route('/report')
@login_required
@roles_required('Admin')
def report():
    return render_template('Admin_page/report.html')