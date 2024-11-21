from flask import Flask, request, jsonify, render_template
import sqlite3

courier = Flask(__name__)

DATABASE = 'courier.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courier_services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                address TEXT NOT NULL
            )
        ''')
        conn.commit()

@courier.route('/courier', methods=['GET', 'POST'])
def index_or_register_courier():
    if request.method == 'GET':
        return render_template('courier-regist.html')
    elif request.method == 'POST':
        try:
            data = request.form
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')
            address = data.get('address')

            if not name or not email or not phone or not address:
                return jsonify({'error': 'All fields are required!'}), 400

            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO courier_services (name, email, phone, address)
                    VALUES (?, ?, ?, ?)
                ''', (name, email, phone, address))
                conn.commit()

            return jsonify({'message': 'Courier service registered successfully!'}), 201
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Email already exists!'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    courier.run(host="127.0.0.1",port="8080",debug=True)