from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'admin_auth.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_number TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_default_admin():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
 
    role_number = "111"
    password = "kalai"
    hashed_password = generate_password_hash(password)
    try:
        cursor.execute('INSERT INTO admin (role_number, password) VALUES (?, ?)', (role_number, hashed_password))
    except sqlite3.IntegrityError:
        pass 
    conn.commit()
    conn.close()

@app.route('/login')
def home():
    return render_template('login-auth.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role_number = request.form['role_number']
        password = request.form['password']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admin WHERE role_number = ?', (role_number,))
        admin = cursor.fetchone()
        conn.close()

        if admin and check_password_hash(admin[2], password):
            session['admin_logged_in'] = True
            session['role_number'] = role_number
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid role number or password', 'danger')
    
    return render_template('login-auth.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        flash('Please log in to access the dashboard', 'warning')
        return redirect(url_for('login'))
    return f"Welcome to the admin dashboard, {session['role_number']}!"

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    add_default_admin()
    app.run(debug=True)