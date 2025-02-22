import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import app

UPLOAD_FOLDER = os.path.join(app.root_path, 'static/sounds')
ALLOWED_EXTENSIONS = {'mp3', 'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/setting', methods=['GET', 'POST'])
def setting():
    if request.method == 'POST':
        if 'sound_file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)

        file = request.files['sound_file']

        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'alert.mp3')  # แทนที่ไฟล์เดิม
            file.save(save_path)
            flash('Sound updated successfully!', 'success')
            return redirect(url_for('setting'))

    return render_template('Admin_page/setting.html')