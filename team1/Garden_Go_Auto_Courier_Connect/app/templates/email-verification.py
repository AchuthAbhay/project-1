from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_password'
mail = Mail(app)

serializer = URLSafeTimedSerializer(app.secret_key)

DATABASE = 'email-verification.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_verified INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/email')
def home():
    return render_template('email-verification.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO customer (name, email, password) VALUES (?, ?, ?)', 
                           (name, email, password))
            conn.commit()
        except sqlite3.IntegrityError:
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('register'))
        conn.close()

        token = serializer.dumps(email, salt='email-confirmation-salt')

        verification_url = url_for('verify_email', token=token, _external=True)
        send_verification_email(email, verification_url)

        flash('Registration successful! Please check your email to verify your account.', 'success')
        return redirect(url_for('home'))
    
    return render_template('email-verification.html')

@app.route('/verify_email/<token>')
def verify_email(token):
    try:
        email = serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except Exception:
        flash('The verification link is invalid or has expired.', 'danger')
        return redirect(url_for('home'))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE customer SET is_verified = 1 WHERE email = ?', (email,))
    conn.commit()
    conn.close()

    flash('Your email has been verified. You can now log in.', 'success')
    return redirect(url_for('home'))

def send_verification_email(email, verification_url):
    msg = Message('Verify Your Email', sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f"Thank you for registering! Please verify your email using the link below:\n{verification_url}"
    mail.send(msg)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)