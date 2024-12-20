from datetime import datetime, timezone
from flask import Blueprint, flash, jsonify, make_response, redirect, render_template, request, send_from_directory, url_for
from flask_mail import Message
from models import User
from flask_login import login_user, login_required, logout_user, current_user
from app import bcrypt, login_manager, mail, serializer, db


app = Blueprint("authenticate",__name__)

@app.route('/')
def home():
    if current_user.is_authenticated:
        print(current_user)
        if current_user.role == "admin":
            response = make_response(redirect(url_for('admin.admin_dashboard')))
        elif current_user.role == "courier_service_provider":
            response = make_response(redirect(url_for('courier.courier_dashboard')))
        else:
            response = make_response(redirect(url_for('customer.show_products')))
        return no_cache(response)
    return render_template('home_page_t1.html')

#Helper function to prevent catching
def no_cache(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, private, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if current_user.is_authenticated:
        logout_user()
    if request.method == 'POST':
        # Determine which form was submitted
        if 'register_btn' in request.form:
            # Registration logic
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role')

            # Check if email already exists
            if User.query.filter_by(email=email).first():
                flash("Email already registered!", "danger")
                return redirect(url_for('authenticate.auth'))

            # Create a new user
            new_user = User(name=name, email=email, password=password, role=role)
            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful!", "success")
            return redirect(url_for('authenticate.auth'))

        elif 'login_btn' in request.form:
            # Login logic
            email = request.form.get('email')
            password = request.form.get('password')

            # Fetch the user
            user = User.query.filter_by(email=email).first()
            if not user or not bcrypt.check_password_hash(user.password_hash, password):
                flash("Invalid email or password", "danger")
                return redirect(url_for('authenticate.auth'))

            # Update last login timestamp
            user.last_login = datetime.now(timezone.utc)
            db.session.commit()

            # Log the user in
            login_user(user)
            flash("Login successful!", "success")

            # Redirect based on user role
            if user.role == "admin":
                return redirect(url_for('admin.admin_dashboard'))
            elif user.role == "courier_service_provider":
                return redirect(url_for('courier.courier_dashboard'))
            else:
                return redirect(url_for('customer.show_products'))

    response = make_response(render_template('auth_t1.html'))
    return no_cache(response)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    response = make_response(redirect(url_for('authenticate.home')))
    return no_cache(response)

@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        email = request.form['email']
        user_mail = User.query.filter(User.email == email).first()
        if not user_mail:
            flash("Email not found. Enter registered email")
            return redirect(url_for('authenticate.forget_password'))
        
        token = serializer.dumps(email, salt='password-reset')
        reset_url = url_for('reset_password', token=token, _external=True)
        msg = Message('Password Reset Request', sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = f'Click the link to reset your password: {reset_url}'
        mail.send(msg)
        flash('A password reset link has been sent to your email.', 'info')
        return redirect(url_for('login'))
    return render_template('forget_password_t1.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset', max_age=3600)
    except Exception:
        flash('The reset link is invalid or has expired.', 'danger')
        return redirect(url_for('authenticate.forget_password'))

    if request.method == 'POST':
        new_password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
            db.session.commit()
            flash('Your password has been reset successfully!', 'success')
            return redirect(url_for('authenticate.login'))

    return render_template('reset_password_t1.html', token=token)

@app.before_request
def update_last_login():
    if current_user.is_authenticated:
        current_user.last_login = datetime.now(timezone.utc)
        db.session.commit()