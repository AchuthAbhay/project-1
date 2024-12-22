from flask import Blueprint, render_template, jsonify, request, current_app
from flask_login import login_required
from analyticsQuery import (
    get_total_sales,
    get_total_profit,
    get_average_order_price,
    get_total_sales_by_category,
    get_availability_count,
    get_daily_profit,
    get_daily_sales,
    get_top_performing_products,
    get_sales_for_filtered_season,
    get_customer_count_by_location,
    get_repeat_customer_rate,
    get_monthly_customer_counts,
    get_delivery_performance
)

from app import db, create_app



# Create a blueprint for API routes
analytics_bp = Blueprint('api', __name__)



# Route to render the dashboard HTML template
@analytics_bp.route('/analytics')
@login_required
def analytics():
    return render_template('dashboard.html')

# API route to fetch total sales data
@analytics_bp.route('/api/total_sales', methods=['GET'])
def total_sales():
    app = create_app()
    with app.app_context():
        session = db.session
        # session = Session
        try:
            data = get_total_sales(session)
            return jsonify({
                "total_sales": "{:.2f}".format(data)
            })
        except Exception as e:
            current_app.logger.error(f"Error in total_sales: {e}")
            return jsonify({"error": "Failed to fetch total sales data"}), 500
        finally:
            session.close()

# API route to fetch total profit data
@analytics_bp.route('/api/total_profit', methods=['GET'])
def total_profit():
    app = create_app()
    with app.app_context():
        session = db.session
        try:
            data = get_total_profit(session)
            return jsonify({
                "total_profit": "{:.2f}".format(data)
            })
        except Exception as e:
            current_app.logger.error(f"Error in total_profit: {e}")
            return jsonify({"error": "Failed to fetch total profit data"}), 500
        finally:
            session.close()

# API route to fetch average order price data
@analytics_bp.route('/api/average_order_price', methods=['GET'])
def average_order_price():
    app = create_app()
    with app.app_context():
        session = db.session 
        try:
            data = get_average_order_price(session)
            return jsonify({
                "average_order_price": "{:.2f}".format(data)
            })
        except Exception as e:
            current_app.logger.error(f"Error in average_order_price: {e}")
            return jsonify({"error": "Failed to fetch average order price"}), 500
        finally:
            session.close()

# API route to fetch total sales by category
@analytics_bp.route('/api/total_sales_by_category', methods=['GET'])
def total_sales_by_category():
    app = create_app()
    with app.app_context():
        session = db.session
        try:
            data = get_total_sales_by_category(session)
            return jsonify([{
                "category": row[0],
                "total_sales": row[1]
            } for row in data])
        except Exception as e:
            current_app.logger.error(f"Error in total_sales_by_category: {e}")
            return jsonify({"error": "Failed to fetch total sales by category"}), 500
        finally:
            session.close()

# API route to fetch product availability data
@analytics_bp.route('/api/product_availability', methods=['GET'])
def product_availability():
    app = create_app()
    with app.app_context():
        session = db.session
        try:
            data = get_availability_count(session)
            return jsonify([{
                "product": row[0],
                "availability_count": row[1]
            } for row in data])
        except Exception as e:
            current_app.logger.error(f"Error in product_availability: {e}")
            return jsonify({"error": "Failed to fetch product availability"}), 500
        finally:
            session.close()

# API route to fetch daily profit data
@analytics_bp.route('/api/daily_profit', methods=['GET'])
def daily_profit():
    app = create_app()
    with app.app_context():
        session = db.session
        try:
            data = get_daily_profit(session)
            return jsonify([{
                "date": row[0],
                "daily_profit": row[1]
            } for row in data])
        except Exception as e:
            current_app.logger.error(f"Error in daily_profit: {e}")
            return jsonify({"error": "Failed to fetch daily profit"}), 500
        finally:
            session.close()

# API route to fetch daily sales data
@analytics_bp.route('/api/daily_sales', methods=['GET'])
def daily_sales():
    app = create_app()
    with app.app_context():
        session = db.session
        try:
            data = get_daily_sales(session)
            return jsonify([{
                "sale_date": row[0],
                "total_sales": row[1]
            } for row in data])
        except Exception as e:
            current_app.logger.error(f"Error in daily_sales: {e}")
            return jsonify({"error": "Failed to fetch daily sales"}), 500
        finally:
            session.close()

# API route to fetch top performing products
@analytics_bp.route('/api/top_performing_products', methods=['GET'])
def top_performing_products():
    app = create_app()
    with app.app_context():
        session = db.session
        try:
            data = get_top_performing_products(session)
            return jsonify([{
                "product_name": row[0],
                "total_sales": row[1]
            } for row in data])
        except Exception as e:
            current_app.logger.error(f"Error in top_performing_products: {e}")
            return jsonify({"error": "Failed to fetch top performing products"}), 500
        finally:
            session.close()

# API Endpoint to get sales for a filtered season
@analytics_bp.route('/api/sales/season', methods=['GET'])
def api_get_sales_for_filtered_season():
    app = create_app()
    with app.app_context():
        session = db.session
        season = request.args.get('season')  # Get season filter from query params
        if not season:
            return jsonify({"error": "Season parameter is required"}), 400
        
        try:
            data = get_sales_for_filtered_season(session, season)
            response = jsonify([{
                "product_name": row[0],
                "total_sales": row[1]
            } for row in data])
            if len(data):
                return response
            else:
                return jsonify([{"product_name": "null", "total_sales":0}])
        except Exception as e:
            current_app.logger.error(f"Error in sales_for_filtered_season: {e}")
            return jsonify({"error": "Failed to fetch sales for the given season"}), 500
        finally:
            session.close()
        
@analytics_bp.route('/api/customers/location', methods=['GET'])
def api_get_customer_count_by_location():
    app = create_app()
    with app.app_context():
        session = db.session
        region = request.args.get('location')  # Get region filter from query params (optional)
        
        try:
            customers = get_customer_count_by_location(session, region)
            return jsonify([{
                "location": row[0],
                "user_count": row[1]
            } for row in customers])
        except Exception as e:
            current_app.logger.error(f"Error in get_customer_count_by_location: {e}")
            return jsonify({"error": "Failed to fetch customer count by location"}), 500
        finally:
            session.close()

# API route to fetch repeat customer rate
@analytics_bp.route('/api/repeat_customer_rate', methods=['GET'])
def repeat_customer_rate():
    app = create_app()
    with app.app_context():
        session = db.session
        try:
            data = get_repeat_customer_rate(session)
            return jsonify({
                "repeat_customer_rate": "{:.0f}%".format(data)
            })
        except Exception as e:
            current_app.logger.error(f"Error in repeat_customer_rate: {e}")
            return jsonify({"error": "Failed to fetch repeat customer rate"}), 500
        finally:
            session.close()

# API route to fetch monthly customer counts
@analytics_bp.route('/api/monthly_customer_counts', methods=['GET'])
def api_get_monthly_customer_counts():
    app = create_app()
    with app.app_context():
        session = db.session
        try:
            data = get_monthly_customer_counts(session)
            return jsonify([{
                "month": row[0],
                "new_customers": row[1],
                "old_customers": row[2]
            } for row in data])
        except Exception as e:
            current_app.logger.error(f"Error in monthly_customer_counts: {e}")
            return jsonify({"error": "Failed to fetch monthly customer counts"}), 500
        finally:
            session.close()

# API route to fetch delivery performance
@analytics_bp.route('/api/delivery_performance', methods=['GET'])
def delivery_performance():
    app = create_app()
    with app.app_context():
        session = db.session
        try:
            data = get_delivery_performance(session)
            on_time_count, late_count = data
            return jsonify([
                {
                    "delivery_type": "On-Time",
                    "count": on_time_count
                },
                {
                    "delivery_type": "Late",
                    "count": late_count
                }
            ])
        except Exception as e:
            current_app.logger.error(f"Error in delivery_performance: {e}")
            return jsonify({"error": "Failed to fetch delivery performance"}), 500
        finally:
            session.close()
