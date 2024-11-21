from flask import Flask, render_template, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker
from dbsetup import create_database
from data import (
    get_total_sales,
    get_total_sales_by_category,
    get_availability_count,
    get_daily_profit,
    get_daily_sales,
    get_top_performing_products
)

# Initialize the Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize database and scoped session
engine = create_database()
Session = scoped_session(sessionmaker(bind=engine))

# Route to render the dashboard HTML template
@app.route('/')
def dashboard():
    return render_template('index.html')

# API route to fetch total sales data
@app.route('/api/total_sales', methods=['GET'])
def total_sales():
    session = Session()
    try:
        data = get_total_sales(session)
        return jsonify([{
            "category": row[0],
            "product": row[1],
            "total_sales": row[2]
        } for row in data])
    except Exception as e:
        app.logger.error(f"Error in total_sales: {e}")
        return jsonify({"error": "Failed to fetch total sales data"}), 500
    finally:
        session.close()

# API route to fetch total sales by category
@app.route('/api/total_sales_by_category', methods=['GET'])
def total_sales_by_category():
    session = Session()
    try:
        data = get_total_sales_by_category(session)
        return jsonify([{
            "category": row[0],
            "total_sales": row[1]
        } for row in data])
    except Exception as e:
        app.logger.error(f"Error in total_sales_by_category: {e}")
        return jsonify({"error": "Failed to fetch total sales by category"}), 500
    finally:
        session.close()

# API route to fetch product availability data
@app.route('/api/product_availability', methods=['GET'])
def product_availability():
    session = Session()
    try:
        data = get_availability_count(session)
        return jsonify([{
            "product": row[1],
            "availability_count": row[2]
        } for row in data])
    except Exception as e:
        app.logger.error(f"Error in product_availability: {e}")
        return jsonify({"error": "Failed to fetch product availability"}), 500
    finally:
        session.close()

# API route to fetch daily profit data
@app.route('/api/daily_profit', methods=['GET'])
def daily_profit():
    session = Session()
    try:
        data = get_daily_profit(session)
        return jsonify([{
            "date": row[0].isoformat(),
            "daily_profit": row[1]
        } for row in data])
    except Exception as e:
        app.logger.error(f"Error in daily_profit: {e}")
        return jsonify({"error": "Failed to fetch daily profit"}), 500
    finally:
        session.close()

# API route to fetch daily sales data
@app.route('/api/daily_sales', methods=['GET'])
def daily_sales():
    session = Session()
    try:
        data = get_daily_sales(session)
        return jsonify([{
            "total_sales": row[0],
            "sale_date": row[1].isoformat()
        } for row in data])
    except Exception as e:
        app.logger.error(f"Error in daily_sales: {e}")
        return jsonify({"error": "Failed to fetch daily sales"}), 500
    finally:
        session.close()
        
# API route to fetch top performing products
@app.route('/api/top_performing_products', methods=['GET'])
def top_performing_products():
    session = Session()
    try:
        data = get_top_performing_products(session)
        return jsonify([{
            "product_name": row[0],
            "total_sales": row[1]
        } for row in data])
    except Exception as e:
        app.logger.error(f"Error in top_performing_products: {e}")
        return jsonify({"error": "Failed to fetch top performing products"}), 500
    finally:
        session.close()



# Teardown session after each request
@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

