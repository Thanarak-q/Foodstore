import os
from flask import Flask, render_template, request, redirect, url_for, flash
from app import app

@app.route('/report')
def report():
    return render_template('Admin_page/report.html')