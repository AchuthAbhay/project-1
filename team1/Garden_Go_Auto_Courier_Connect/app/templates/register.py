from flask import Flask, render_template, request, redirect, flash
import sqlite3

register = Flask(__name__) 
register.secret_key = 'your_secret_key' 

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@register.route('/')
def home():
    return redirect('/register')

@register.route('/register', methods=['GET', 'POST'])
def register_route():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        if not name or not email or not password: 
            flash('All fields are required!')
            return redirect('/register')
        
        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('INSERT INTO customers (name, email, password) VALUES (?, ?, ?)', 
                      (name, email, password))
            conn.commit()
            conn.close()
            flash('Registration successful!')
            return redirect('/register')
        except sqlite3.IntegrityError:
            flash('Email already exists. Please use a different email.')
            return redirect('/register')

    return render_template('register.html')

if __name__ == '__main__':
    init_db()
    register.run(debug=True)