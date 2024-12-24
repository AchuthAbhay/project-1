from sqlalchemy import func, extract, desc, case
from models import OrderItem, Order, Product, Category, User
from app import db
from app import create_app

# Function to Retrieve the total profit
def get_total_profit(session):
    """Retrieve the total profit."""
    total_profit = session.query(
        func.sum(
            (Product.selling_price - Product.cost_price) * OrderItem.quantity
        ).label("total_profit")
    ).select_from(OrderItem).join(
        Product, OrderItem.product_id == Product.product_id
    ).scalar()

    return total_profit

# Function to Retrieve average order price
def get_average_order_price(session):
    """Retrieve the average total_price of orders."""
    average_total_price = session.query(
        func.avg(Order.total_price).label("average_total_price")
    ).scalar()

    return average_total_price

# Function to get sales for filtered season
def get_sales_for_filtered_season(session, season_filter, limit=6):
    season_months = {
        'all': (1, 12),
        'spring': (3, 5),
        'summer': (6, 8),
        'autumn': (9, 11),
        'winter': (12, 2)
    }

    if season_filter not in season_months:
        raise ValueError(f"Invalid season '{season_filter}'. Valid options are: {', '.join(season_months.keys())}")

    start_month, end_month = season_months[season_filter]

    query = session.query(
        Product.name,
        func.sum(OrderItem.quantity * Product.selling_price).label('total_sales')
    ).join(OrderItem, Product.product_id == OrderItem.product_id
    ).join(Order, Order.order_id == OrderItem.order_id
    ).filter(
        extract('month', Order.created_at).between(start_month, end_month)
    ).group_by(
        Product.name
    ).order_by(
        desc('total_sales')  # Order by total_sales in descending order
    )
    
    if limit:
        query = query.limit(limit)  # Apply limit if provided

    results = query.all()
    return results

# Function to get customer count by region
def get_customer_count_by_region(session, region_filter=None):
    query = session.query(User.region, func.count(User.user_id).label('total_customers'))

    if region_filter:
        query = query.filter(User.region.like(f'%{region_filter}%'))

    query = query.group_by(User.region)

    results = query.all()
    return results

# Function to get total sales
def get_total_sales(session):
    total_sales = session.query(
        func.sum(OrderItem.quantity * Product.selling_price).label("total_sales")
    ).join(Product, OrderItem.product_id == Product.id).scalar()
    return total_sales

# Function to get total sales by category
def get_total_sales_by_category(session):
    total_sales_by_category = session.query(
        Category.category_name,
        func.sum(OrderItem.quantity * Product.selling_price).label("total_sales")
    ).join(Product, Product.category_id == Category.category_id
    ).join(OrderItem, OrderItem.product_id == Product.product_id
    ).group_by(Category.category_name).all()

    return total_sales_by_category

# Function to get total sales by product
def get_total_sales_by_product(session):
    total_sales_by_product = session.query(
        Product.name,
        func.sum(OrderItem.quantity * Product.selling_price).label("total_sales")
    ).join(OrderItem, OrderItem.product_id == Product.product_id
    ).group_by(Product.name).all()

    return total_sales_by_product

# Function to get availability count
def get_availability_count(session):
    availability_count = session.query(
        Product.name,
        Product.stock_quantity.label("available_stock")
    ).order_by(
        "available_stock"
    ).all()

    return availability_count

# Function to get daily profit
def get_daily_profit(session):
    daily_profit = session.query(
        func.date(Order.created_at).label("date"),
        func.sum(
            (Product.selling_price - Product.cost_price) * OrderItem.quantity
        ).label("daily_profit")
    ).join(OrderItem, OrderItem.order_id == Order.order_id
    ).join(Product, Product.product_id == OrderItem.product_id
    ).filter(Order.created_at.isnot(None)
    ).group_by(func.date(Order.created_at)).all()

    return daily_profit

# Function to get top performing products
def get_top_performing_products(session, limit=5):
    top_performing_products = session.query(
        Product.name,
        func.sum(OrderItem.quantity).label("total_quantity_sold")
    ).join(OrderItem, Product.product_id == OrderItem.product_id
    ).group_by(Product.name
    ).order_by(func.sum(OrderItem.quantity).desc() 
    ).limit(limit).all()
    return top_performing_products

# Function to get daily sales
def get_daily_sales(session):
    daily_sales = session.query(
        func.date(Order.created_at).label("date"),
        func.sum(OrderItem.quantity).label("daily_sales_volume")
    ).join(OrderItem, OrderItem.order_id == Order.order_id
    ).filter(Order.created_at.isnot(None)
    ).group_by(func.date(Order.created_at)).all()

    return daily_sales

# Function to get customer count by location
def get_customer_count_by_location(session, group_by_column='country'):
    
    if group_by_column == 'country':
        location = User.country
    elif group_by_column == "region":
        location = User.region
    else:
        return f"Invalid Location"
    
    query = session.query(
        location,
        func.count(User.user_id)
    )

    query = query.group_by(location)

    results = query.all()
    return results

# Function to get repeat customer rate
def get_repeat_customer_rate(session):
    
    total_customers = session.query(func.count(func.distinct(Order.user_id))).scalar()
    
    repeat_customers_query = session.query(func.distinct(Order.user_id))\
        .group_by(Order.user_id)\
        .having(func.count(Order.order_id) > 1)
    
    repeat_customers = repeat_customers_query.count()
  
    if total_customers > 0:
        repeat_customer_rate = (repeat_customers / total_customers) * 100
    else:
        repeat_customer_rate = 0  

    return repeat_customer_rate

# Function to get month-wise customer counts
def get_monthly_customer_counts(session):
    """Retrieve month-wise count of new and old customers."""
    result = (
        session.query(
            func.strftime('%Y-%m', Order.created_at).label('month'),  # Extract year-month from order date
            func.count(
                func.distinct(
                    case(
                        # New customers: User created in the same month as the order
                        (func.strftime('%Y-%m', User.created_at) == func.strftime('%Y-%m', Order.created_at), User.user_id)
                    )
                )
            ).label('new_customer_count'),
            func.count(
                func.distinct(
                    case(
                        # Old customers: User created before the order's month
                        (func.strftime('%Y-%m', User.created_at) < func.strftime('%Y-%m', Order.created_at), User.user_id)
                    )
                )
            ).label('old_customer_count'),
        )
        .join(User, User.user_id == Order.user_id)  # Join User and Order tables
        .group_by(func.strftime('%Y-%m', Order.created_at))  # Group by year-month
        .order_by('month')
    ).all()

    return result


# Function to get delivery performance
def get_delivery_performance(session):
    
    on_time_count = session.query(func.count(Order.order_id))\
        .filter(Order.actual_delivery <= Order.estimated_delivery).scalar()

    
    late_count = session.query(func.count(Order.order_id))\
        .filter(Order.actual_delivery > Order.estimated_delivery).scalar()

    return on_time_count, late_count

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        session = db.session

        average_order = get_average_order_price(session)
        print(f"\nAverage Order price: {average_order:.2f}")

        total_profit = get_total_profit(session)
        print(f"\nTotal profit: {total_profit:.2f}")

        total_sales = get_total_sales(session)
        print(f"\nTotal Sales: {total_sales:.2f}")

        total_sales_by_category = get_total_sales_by_category(session)
        print("\nTotal Sales by Category:")
        for category, sales in total_sales_by_category:
            print(f"Category: {category}, Total Sales: {sales}")

        total_sales_by_product = get_total_sales_by_product(session)
        print("\nTotal Sales by Product:")
        for product, sales in total_sales_by_product:
            print(f"Product: {product}, Total Sales: {sales}")

        availability_count = get_availability_count(session)
        print("\nAvailability Count:")
        for product, stock in availability_count:
            print(f"Product: {product}, Available Stock: {stock}")

        daily_profit = get_daily_profit(session)
        print("\nDaily Profit:")
        for date, profit in daily_profit:
            print(f"Date: {date}, Daily Profit: {profit}")

        daily_sales = get_daily_sales(session)
        print("\nDaily Sales:")
        for date, sales in daily_sales:
            print(f"Date: {date}, Daily Sales Volume: {sales}")

        print("\nTop Performing Products:")
        top_performing_products = get_top_performing_products(session, limit=5)
        for product, total_sold in top_performing_products:
            print(f"Product: {product}, Total Quantity Sold: {total_sold}")
            
        customer_count_by_location = get_customer_count_by_location(session)
        print("\ncustomer count by location")
        for location, user_count  in customer_count_by_location:
            print(f"Location: {location}, User_count: {user_count}")

        print("\nSales for Filtered Season")
        print(get_sales_for_filtered_season(session, 'summer'))
        for product, total_sales in get_sales_for_filtered_season(session, 'summer'):
            print(f"Product: {product}, Total_sales: {total_sales}")

        repeat_customer_rate = get_repeat_customer_rate(session)
        print(f"\nRepeat Customer Rate: {repeat_customer_rate:.2f}%")

        repeat_customer_rate_monthly = get_monthly_customer_counts(session)
        print("\nMonth-wise New Customers and Old Customers:")
        for month, new, old in repeat_customer_rate_monthly:
            print(f"Month: {month}, New_Customers: {new}, Old_Customers: {old}")