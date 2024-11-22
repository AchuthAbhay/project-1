from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Courier(db.Model):
    __tablename__ = 'courier'
    courier_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)
    vehicle_info = db.Column(db.String(100))
    vehicle_no = db.Column(db.String(100))
    assigned_orders_count = db.Column(db.Integer, default=0)

    orders = db.relationship('Order', back_populates='courier', lazy='dynamic')
    audit_logs = db.relationship('Audit', back_populates='courier', lazy='dynamic')

class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_address = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(15), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    courier_id = db.Column(db.Integer, db.ForeignKey('courier.courier_id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    estimated_delivery = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    courier = db.relationship('Courier', back_populates='orders')

    audit_logs = db.relationship('Audit', back_populates='order', lazy='dynamic')

class Audit(db.Model):
    __tablename__ = 'audit'
    record_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_by = db.Column(db.Integer, db.ForeignKey('courier.courier_id'), nullable=False)
    reason = db.Column(db.Text)

    order = db.relationship('Order', back_populates='audit_logs')
    courier = db.relationship('Courier', back_populates='audit_logs')

