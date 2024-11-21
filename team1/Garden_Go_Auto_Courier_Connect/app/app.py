from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)

service_providers = {
    1: {"name": "John Doe", "service": "Plumbing"},
    2: {"name": "Jane Smith", "service": "Electrical Work"},
    3: {"name": "Bob Johnson", "service": "Carpentry"}
}

@app.route('/contact/<int:provider_id>', methods=['GET', 'POST'])
def contact_provider(provider_id):
    provider = service_providers.get(provider_id)
    if not provider:
        return "Service Provider Not Found", 404

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Handle the message (e.g., save it to a database or send an email)
        return f"Thank you, {name}! Your message has been sent to {provider['name']}."

    return render_template('contact.html', provider_name=provider['name'], provider_id=provider_id)


@app.route('/')
def homePage():
    return render_template('home_page.html')
@app.route('/register')
def home():
    return render_template('register.html')
@app.route('/register/admin', methods=['GET', 'POST'])
def register_admin():
    return render_template('admin_registration.html')
@app.route('/register/user', methods=['GET', 'POST'])
def register_user():
    return render_template('user_registration.html')
@app.route('/register/courier_service_provider', methods=['GET', 'POST'])
def register_courier_service_prodiver():
    return render_template('courier_registration.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
@app.route('/track_order', methods=['GET', 'POST'])
def track_order():
    return render_template('track_order.html')
@app.route('/profile_completion', methods=['GET', 'POST'])
def profile_completion():
    return render_template('profile_completion.html')

@app.route('/customer_dashboard',methods=['GET', 'POST'])
def customer_dashboard():
    return render_template('customer_dashboard.html')

@app.route('/products',methods=['GET', 'POST'])
def products():
    return render_template('products.html')

@app.route('/contact',methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

if "__main__"==__name__:
    app.run(debug=True)

