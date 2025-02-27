import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app import app
from werkzeug.utils import secure_filename
from app.models.store import Store
from app.controllers.role_controller import roles_required



# Define the paths for sounds and logos
SOUNDS_FOLDER = os.path.join(app.static_folder, 'sounds')
LOGO_FOLDER = os.path.join(app.static_folder, 'ico')

# Ensure the directories exist
os.makedirs(SOUNDS_FOLDER, exist_ok=True)
os.makedirs(LOGO_FOLDER, exist_ok=True)

@app.route('/setting', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def setting():
    if request.method == 'POST':
        # Handle file uploads and form data here
        if 'name' in request.form:
            print("eieieiieieieieiei")
            name = str(request.form['name'])
            store = Store.query.first()
            if store:
                store.update_name(name)

        if 'cooking_sound' in request.files:
            cooking_sound = request.files['cooking_sound']
            if cooking_sound.filename != '':
                filename = "cooking_room.mp3"
                cooking_sound.save(os.path.join(SOUNDS_FOLDER, filename))
                flash('Cooking room sound uploaded successfully!', 'success')

        if 'waiter_sound' in request.files:
            waiter_sound = request.files['waiter_sound']
            if waiter_sound.filename != '':
                filename = "waiter.mp3"
                waiter_sound.save(os.path.join(SOUNDS_FOLDER, filename))
                flash('Waiter sound uploaded successfully!', 'success')

        if 'logo_file' in request.files:
            logo_file = request.files['logo_file']
            if logo_file.filename != '':
                filename = "logo.jpg"
                logo_file.save(os.path.join(LOGO_FOLDER, filename))
                flash('Logo uploaded successfully!', 'success')

        # Handle vat and service charge updates
        if 'vat_rate' in request.form:
            vat_rate = float(request.form['vat_rate'])
            store = Store.query.first() 
            if store:
                store.update_vat(vat_rate)

        if 'service_charge' in request.form:
            service_charge = float(request.form['service_charge'])
            store = Store.query.first()
            if store:
                store.update_service_charge(service_charge)

        # Handle order settings updates
        if 'max_orders' in request.form:
            max_orders = int(request.form['max_orders'])
            store = Store.query.first()
            if store:
                store.update_max_orders(max_orders)

        if 'max_food_quantity' in request.form:
            max_food_quantity = int(request.form['max_food_quantity'])
            store = Store.query.first()
            if store:
                store.update_max_food(max_food_quantity)

        return redirect(url_for('setting'))

    # Render the template
    store = Store.query.first()
    return render_template('Admin_page/setting.html', store=store)



@app.route("/store_list")
def store_list():
    store = []
    db_store = Store.query.all()
    store = list(map(lambda x: x.to_dict(), db_store))
    app.logger.debug("DB store (Sorted): " + str(store))
    return jsonify(store)