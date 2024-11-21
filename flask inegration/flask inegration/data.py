from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dbsetup import Category, Product, SalesPerformance,ProductAvailability,ProfitTrend



def get_session():
    database_url = "sqlite:///gardengo.db"
    engine = create_engine(database_url, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()



def get_total_sales(session):
    total_sales = (
        session.query(
            Category.category_name,
            Product.product_name,
            func.sum(SalesPerformance.total_sales).label("total_sales")
        )
        .join(Product, Category.category_id == Product.category_id)
        .join(SalesPerformance, Product.product_id == SalesPerformance.product_id)
        .group_by(Category.category_name, Product.product_name)
        .order_by(Category.category_name, Product.product_name)
        .all()
    )
    return total_sales

def get_total_sales_by_category(session):
    total_category_sale= (
             session.query(
                Category.category_name,
                func.sum(SalesPerformance.total_sales).label("total_sales")
            )
            .join(Product, Category.category_id == Product.category_id)
            .join(SalesPerformance, Product.product_id == SalesPerformance.product_id)
            .group_by(Category.category_name)
            .order_by(Category.category_name)
            .all()
        )

    return total_category_sale

def get_availability_count(session):
    results = (
        session.query(
            Category.category_name,
            Product.product_name,
            ProductAvailability.availability_count
        )
        .join(Product, Category.category_id == Product.category_id)
        .join(ProductAvailability, Product.product_id == ProductAvailability.product_id)
        .order_by(Category.category_name, Product.product_name)
        .all()
        )


    return results

def get_daily_profit(session):
    daily_profit = (
        session.query(
            ProfitTrend.date,
            func.sum(ProfitTrend.total_profit).label("daily_profit")
        )
        .group_by(ProfitTrend.date)
        .order_by(ProfitTrend.date)
        .all()
    )
    
    return daily_profit


def get_daily_sales(session):
    today = datetime.today()

    daily_sales = (
        session.query(
            func.sum(SalesPerformance.total_sales).label("total_sales"),
            SalesPerformance.date.label("sale_date")  # group by date
        )
        .group_by(func.date(SalesPerformance.date))  # only group by date
        .order_by(func.date(SalesPerformance.date))  # order by date
        .all()
    )
    
    return daily_sales



def get_top_performing_products(session, limit=4):
    top_products = (
        session.query(
            Product.product_name,
            func.sum(SalesPerformance.total_sales).label("total_sales")
        )
        .join(SalesPerformance, Product.product_id == SalesPerformance.product_id)
        .group_by(Product.product_name)
        .order_by(desc("total_sales"))  # Order by total sales in descending order
        .limit(limit)  # Limit the results to the top 'n' products
        .all()
    )

    return top_products



if __name__ == "__main__":

    session = get_session()


    total_sales = get_total_sales(session)
    total_category_sale = get_total_sales_by_category(session)
    results = get_availability_count(session)
    daily_profit = get_daily_profit(session)
    daily_sales = get_daily_sales(session)
    top_performing_products = get_top_performing_products(session)

    for category_name, product_name, total_sales in total_sales:
        print(f"Category: {category_name}, Product: {product_name}, Total Sales: {total_sales}")

    for category_name, total_sales in total_category_sale:
        print(f"Category: {category_name}, Total Sales: {total_sales}")

    for category_name,product_name,availability_count in results:
        print(f"Category: {category_name}, Product: {product_name}, Availability_count {availability_count}")


    for sale_date, daily_profit_amount in daily_profit:
        print(f"Date: {sale_date}, Daily Profit: {daily_profit_amount}")

    for total_sales, sale_date in daily_sales:
        print(f"Date: {sale_date}, Total Sales: {total_sales}")
        
    for product_name, total_sales in top_performing_products:
        print(f"Product:{product_name}, Total Sales:{total_sales}")

    session.close()








