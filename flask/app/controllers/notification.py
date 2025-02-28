from app import app
from app import db
from app.models.noti import Noti
from flask import (jsonify, render_template, request, url_for, flash, redirect)

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    # notifications = Noti.query.filter_by(is_read=False).order_by(Noti.created_at.desc()).limit(5).all()
    notifications = Noti.query.filter_by(is_read=False).order_by(Noti.created_at.desc()).all()
    return jsonify([notif.to_dict() for notif in notifications])

@app.route('/api/notifications', methods=['POST'])
def create_notification():
    data = request.get_json()
    new_notif = Noti(
        type=data['type'],
        message=data['message'],
        link=data.get('link'),
        related_id=data.get('related_id')
    )
    db.session.add(new_notif)
    db.session.commit()
    return jsonify(new_notif.to_dict()), 201

@app.route('/api/notifications/<int:notification_id>', methods=['PUT'])
def update_notification(notification_id):
    print("เรียกใช้งานเหี้ย1")
    notif = Noti.query.get_or_404(notification_id)
    data = request.get_json()
    if 'is_read' in data:
        notif.is_read = data['is_read']
    db.session.commit()
    return jsonify(notif.to_dict())

@app.route('/api/notifications/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    notif = Noti.query.get_or_404(notification_id)
    db.session.delete(notif)
    db.session.commit()
    return jsonify({"message": "Noti deleted"}), 200