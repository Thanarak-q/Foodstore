import os
from flask import Flask, render_template, request, redirect, url_for, flash
from app import app
from werkzeug.utils import secure_filename

# Define the paths for sounds and logos
SOUNDS_FOLDER = os.path.join(app.static_folder, 'sounds')
LOGO_FOLDER = os.path.join(app.static_folder, 'ico')

# Ensure the directories exist
os.makedirs(SOUNDS_FOLDER, exist_ok=True)
os.makedirs(LOGO_FOLDER, exist_ok=True)

@app.route('/setting', methods=['GET', 'POST'])
def setting():
    if request.method == 'POST':
        # Handle sound file upload for cooking room
        if 'cooking_sound' in request.files:
            cooking_sound = request.files['cooking_sound']
            if cooking_sound.filename != '':
                filename = "cooking_room.mp3"  # Fixed filename for cooking sound
                cooking_sound.save(os.path.join(SOUNDS_FOLDER, filename))
                flash('Cooking room sound uploaded successfully!', 'success')

        # Handle sound file upload for waiter
        if 'waiter_sound' in request.files:
            waiter_sound = request.files['waiter_sound']
            if waiter_sound.filename != '':
                filename = "waiter.mp3"  # Fixed filename for waiter sound
                waiter_sound.save(os.path.join(SOUNDS_FOLDER, filename))
                flash('Waiter sound uploaded successfully!', 'success')

        # Handle logo file upload
        if 'logo_file' in request.files:
            logo_file = request.files['logo_file']
            if logo_file.filename != '':
                filename = "logo.jpg"  # Fixed filename for logo
                logo_file.save(os.path.join(LOGO_FOLDER, filename))
                flash('Logo uploaded successfully!', 'success')

        return redirect(url_for('setting'))

    return render_template('Admin_page/setting.html')