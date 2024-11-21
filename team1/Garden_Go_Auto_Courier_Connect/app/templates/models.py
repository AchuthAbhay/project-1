from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define User table (first table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    shipping_address = db.Column(db.JSON, nullable=True)  # JSON field for multiple addresses
    role = db.Column(db.String(50), nullable=False)
    token_id = db.Column(db.String(255), nullable=True)  # Token ID for admin
    profile_update_at = db.Column(db.DateTime, nullable=True)  # Only for customers
    created_at = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)

# Define Password Reset table (second table)
class PasswordReset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    p_token_id = db.Column(db.String(255), nullable=False)
    p_token = db.Column(db.String(255), nullable=False)
    p_created_at = db.Column(db.DateTime, nullable=False)
    p_expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
