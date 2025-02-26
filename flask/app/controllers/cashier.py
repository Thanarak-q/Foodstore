from flask import Flask, render_template, request

from app import app

@app.route('/cashier')
def cashier_index():
    return render_template('cashier_page/index.html')



@app.route('/cashier/invoice')
def invoice():
    table_id = request.args.get('table_id')
    qrcode = request.args.get('qrcode')
    return render_template('cashier_page/invoice.html', table_id=table_id, qrcode=qrcode)




# @app.route('/cashier/invoice/download')