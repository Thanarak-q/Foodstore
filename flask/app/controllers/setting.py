from flask import Flask, render_template
from app import app

@app.route('/setting')
def setting():
    return render_template('Admin_page/setting.html')

