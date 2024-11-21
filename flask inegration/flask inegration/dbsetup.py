from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()


class SalesSummary(Base):
    __tablename__ = 'sales_summary'
    date = Column(Date, primary_key=True)
    total_sales_amount = Column(Float, nullable=False)
    total_profit = Column(Float, nullable=False)
    average_sales = Column(Float, nullable=False)
    total_sales_count = Column(Integer, nullable=False)


class ProductAvailability(Base):
    __tablename__ = 'product_availability'
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)
    availability_count = Column(Integer, nullable=False)

    category = relationship('Category', back_populates='product_availability')
    product =relationship('Product',back_populates= 'product_availability')



class CategorySummary(Base):
    __tablename__ = 'category_summary'
    category_id = Column(Integer, ForeignKey('categories.category_id'), primary_key=True)
    products_sold_count = Column(Integer, nullable=False)
    date = Column(Date, primary_key=True)

    category = relationship('Category',back_populates='category_summary')


class ProfitTrend(Base):
    __tablename__ = 'profit_trend'
    date = Column(Date, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    total_profit = Column(Float, nullable=False)
    period = Column(String(255), nullable=False)



    product = relationship('Product', back_populates='profit_trend')


class SalesPerformance(Base):
    __tablename__ = 'sales_performance'
    date = Column(Date, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    total_sales = Column(Float, nullable=False)
    period = Column(String(50), nullable=False)


    product = relationship('Product', back_populates='sales_performance')


class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)

    category = relationship('Category', back_populates='products')
    sales_performance = relationship('SalesPerformance', back_populates='product')
    profit_trend = relationship('ProfitTrend', back_populates='product')
    product_availability = relationship('ProductAvailability', back_populates='product')


class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(255), nullable=False)
    products = relationship('Product', back_populates='category')
    product_availability = relationship('ProductAvailability', back_populates='category')
    category_summary = relationship('CategorySummary', back_populates='category')


def create_database():
    database_url = "sqlite:///gardengo.db"
    engine = create_engine(database_url, echo=True)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == "__main__":
    engine = create_database()
    session = get_session(engine)

    from datetime import date

    categories = [
        Category(category_id=1, category_name="Plants"),
        Category(category_id=2, category_name="Seeds"),
    ]

    products = [
        Product(product_id=1, product_name="Rose plant", category_id=1),
        Product(product_id=2, product_name="Basil plant", category_id=1),
        Product(product_id=3, product_name="Mint plant", category_id=1),
        Product(product_id=4, product_name="Sunflower seeds", category_id=2),
        Product(product_id=5, product_name="Tomato seeds", category_id=2),
        Product(product_id=6, product_name="Lavender seeds", category_id=2),
        Product(product_id=7, product_name="Pumpkin seeds", category_id=2),
        Product(product_id=8, product_name="Aloe plant", category_id=1),
        Product(product_id=9, product_name="Basil seeds", category_id=2),
    ]

    sales_summaries = [
        SalesSummary(date=date(2024, 11, 13), total_sales_amount=10000.0, total_profit=3000.0, average_sales=500.0, total_sales_count=20),
        SalesSummary(date=date(2024, 11, 14), total_sales_amount=15000.0, total_profit=4000.0, average_sales=750.0, total_sales_count=30)
    ]

    profit_trends = [
        ProfitTrend(date=date(2024, 11, 11), product_id=1, total_profit=500.0, period="Daily"),
        ProfitTrend(date=date(2024, 11, 11), product_id=2, total_profit=700.0, period="Daily"),
        ProfitTrend(date=date(2024, 11, 12), product_id=3, total_profit=300.0, period="Daily"),
        ProfitTrend(date=date(2024, 11, 12), product_id=4, total_profit=400.0, period="Daily"),
        ProfitTrend(date=date(2024, 11, 13), product_id=5, total_profit=250.0, period="Daily"),
        ProfitTrend(date=date(2024, 11, 13), product_id=6, total_profit=150.0, period="Daily"),
        ProfitTrend(date=date(2024, 11, 13), product_id=7, total_profit=600.0, period="Daily"),
        ProfitTrend(date=date(2024, 11, 13), product_id=8, total_profit=550.0, period="Daily"),
        ProfitTrend(date=date(2024, 11, 13), product_id=9, total_profit=500.0, period="Daily")
    ]

    sales_performances = [
        SalesPerformance(date=date(2024, 11, 11), product_id=1, total_sales=1000.0, period="Daily"),
        SalesPerformance(date=date(2024, 11, 11), product_id=2, total_sales=1500.0, period="Daily"),
        SalesPerformance(date=date(2024, 11, 12), product_id=3, total_sales=800.0, period="Daily"),
        SalesPerformance(date=date(2024, 11, 12), product_id=4, total_sales=900.0, period="Daily"),
        SalesPerformance(date=date(2024, 11, 13), product_id=5, total_sales=700.0, period="Daily"),
        SalesPerformance(date=date(2024, 11, 13), product_id=6, total_sales=600.0, period="Daily"),
        SalesPerformance(date=date(2024, 11, 13), product_id=7, total_sales=1200.0, period="Daily"),
        SalesPerformance(date=date(2024, 11, 13), product_id=8, total_sales=1100.0, period="Daily"),
        SalesPerformance(date=date(2024, 11, 13), product_id=9, total_sales=1000.0, period="Daily")
    ]

    product_availabilities = [
        ProductAvailability(product_id=1, category_id=1, availability_count=50),
        ProductAvailability(product_id=2, category_id=1, availability_count=30),
        ProductAvailability(product_id=3, category_id=1, availability_count=100),
        ProductAvailability(product_id=4, category_id=2, availability_count=20),
        ProductAvailability(product_id=5, category_id=2, availability_count=15),
        ProductAvailability(product_id=6, category_id=2, availability_count=40),
        ProductAvailability(product_id=7, category_id=2, availability_count=200),
        ProductAvailability(product_id=8, category_id=1, availability_count=150),
        ProductAvailability(product_id=9, category_id=2, availability_count=80),
    ]

    category_summaries = [
        CategorySummary(category_id=1, products_sold_count=100, date=date(2024, 11, 13)),
        CategorySummary(category_id=2, products_sold_count=50, date=date(2024, 11, 13))
    ]

    session.add_all(categories + products + sales_summaries + category_summaries + product_availabilities + sales_performances + profit_trends)
    session.commit()
