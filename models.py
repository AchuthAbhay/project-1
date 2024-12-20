from datetime import datetime, timezone
# from app import db, bcrypt
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


db = SQLAlchemy()
bcrypt = Bcrypt()
Base = declarative_base()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    profile_updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    address = db.Column(db.String(300))
    phone_number = db.Column(db.String(15))
    pincode = db.Column(db.String(10))
    region = db.Column(db.String(50))
    country = db.Column(db.String(50))
    vehicle_info = db.Column(db.String(150))
    vehicle_number = db.Column(db.String(50))

    def __init__(self, name, email, password, role, **kwargs):
        self.name = name
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_id(self):
        return str(self.user_id)

    orders_customer = db.relationship("Order", foreign_keys='Order.user_id', back_populates="user")
    orders_courier = db.relationship("Order", foreign_keys='Order.assigned_to', back_populates="courier")
    carts = db.relationship("Cart", back_populates="user")
    password_resets = db.relationship("PasswordReset", back_populates="user")
    subscriptions = db.relationship("Subscription", back_populates="user")
    audit_logs = db.relationship("Audit", back_populates="user")



class PasswordReset(db.Model):
    __tablename__ = 'passwordreset'
    passwordreset_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    ptoken = db.Column(db.String(256), nullable=False, unique=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", back_populates="password_resets")

class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    created_at = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="carts")
    cart_items = db.relationship("CartItem", back_populates="cart")

class CartItem(db.Model):
    __tablename__ = 'cart_item'
    cart_item_id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.cart_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    quantity = db.Column(db.Integer, nullable=False)

    cart = db.relationship("Cart", back_populates="cart_items")
    product = db.relationship("Product", back_populates="cart_items")

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    cost_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String)
    stock_quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))

    category = db.relationship("Category", back_populates="products")
    cart_items = db.relationship("CartItem", back_populates="product")
    order_items = db.relationship("OrderItem", back_populates="product")

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    category_description = db.Column(db.String)

    products = db.relationship("Product", back_populates="category")

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    address = db.Column(db.String(300))
    pincode = db.Column(db.String, nullable=False)
    estimated_delivery = db.Column(db.DateTime)
    actual_delivery = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    total_price = db.Column(db.Float, nullable=False)
    shipping_cost = db.Column(db.Float, nullable=False)

    user = db.relationship("User",foreign_keys=[user_id],back_populates="orders_customer")
    courier = db.relationship("User", foreign_keys=[assigned_to], back_populates="orders_courier")
    order_items = db.relationship("OrderItem", back_populates="order")
    audit_logs = db.relationship("Audit",foreign_keys='Audit.order_id', back_populates="order")

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    quantity = db.Column(db.Integer, nullable=False)

    order = db.relationship("Order", back_populates="order_items")
    product = db.relationship("Product", back_populates="order_items")

class Audit(db.Model):
    __tablename__ = 'audit'
    record_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    reason = db.Column(db.Text)

    order = db.relationship("Order",foreign_keys=[order_id], back_populates="audit_logs")
    user = db.relationship("User", back_populates="audit_logs")

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    subscription_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    endpoint = db.Column(db.String, nullable=False)
    auth = db.Column(db.String, nullable=False)
    p256dh = db.Column(db.String, nullable=False)

    user = db.relationship("User", back_populates="subscriptions")

def create_database():
    database_url = "sqlite:///traildb.db"
    engine = create_engine(database_url, echo=True)
    Base.metadata.create_all(engine)
    return engine

if __name__ == "__main__":
    create_database()
