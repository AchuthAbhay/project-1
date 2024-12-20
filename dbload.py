from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random
from datetime import datetime, timedelta
from models import User, PasswordReset, Cart, CartItem, Product, Category, Order, OrderItem, Audit, Subscription, Base, create_database


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()


def populate_db(session):
    faker = Faker()

    countries = ["USA", "India", "UK", "Canada", "Germany", "Australia", "France", "Japan", "South Korea", "Brazil"]

    regions = ["North", "South", "East", "West"]

    # Create categories
    categories = []
    category_names = ["Seeds", "Plants", "Herbals", "Flowers"]
    for name in category_names:
        category = Category(
            category_name=name,
            category_description=faker.text(max_nb_chars=100)
        )
        categories.append(category)
        session.add(category)
    session.commit()

    # Create products
    products = []
    for _ in range(50):
        category = random.choice(categories)
        product = Product(
            name=f"{faker.word()} {category.category_name.lower()}",
            cost_price=round(random.uniform(5, 200), 2),
            selling_price=round(random.uniform(10, 250), 2),
            description=faker.text(max_nb_chars=200),
            stock_quantity=random.randint(1, 100),
            image_url=faker.image_url(),
            category_id=category.category_id,
            product_weight=round(random.uniform(0.1, 10.0), 2)  # Add product weight (e.g., in kilograms)
        )
        products.append(product)
        session.add(product)


    # Create users
    users = []
    roles = ["admin", "customer", "courier"]
    for _ in range(30):
        user = User(
            name=faker.name(),
            email=faker.email(),
            password_hash=faker.password(),
            role=random.choice(roles),
            created_at=faker.date_this_year(),
            profile_updated_at=faker.date_this_year(),
            last_login=faker.date_this_year(),
            address=faker.address(),
            phone_number=faker.phone_number(),
            pincode=faker.zipcode(),
            region=random.choice(regions), 
            country=random.choice(countries),  
            vehicle_info=faker.word(),
            vehicle_number=faker.license_plate()
        )
        users.append(user)
        session.add(user)
    session.commit()

    # Create password resets
    for user in users:
        password_reset = PasswordReset(
            user_id=user.user_id,
            ptoken=faker.uuid4(),
            expires_at=datetime.now() + timedelta(hours=1),
            created_at=datetime.now()
        )
        session.add(password_reset)
    session.commit()

    # Create orders
    orders = []
    for _ in range(20):
        user = random.choice(users)
        order = Order(
            user_id=user.user_id,
            status=random.choice(['pending', 'completed', 'shipped', 'cancelled']),
            address=user.address,
            estimated_delivery=faker.date_this_year(),
            actual_delivery=faker.date_this_year(),
            updated_at=faker.date_this_year(),
            total_price=round(random.uniform(100, 500), 2),
            shipping_cost=round(random.uniform(5, 50), 2),
            pincode=user.pincode,
            created_at=faker.date_this_year()
        )
        orders.append(order)
        session.add(order)
    session.commit()

    # Create order items
    for order in orders:
        num_items = random.randint(1, 5)
        for _ in range(num_items):
            product = random.choice(products)
            order_item = OrderItem(
                order_id=order.order_id,
                product_id=product.product_id,
                quantity=random.randint(1, 3)
            )
            session.add(order_item)
    session.commit()

    # Create audit logs
    for order in orders:
        audit_log = Audit(
            order_id=order.order_id,
            status="created",
            updated_at=datetime.now(),
            updated_by="system",
            reason="Initial creation"
        )
        session.add(audit_log)
    session.commit()

    # Create subscriptions (push notifications)
    for user in users:
        subscription = Subscription(
            user_id=user.user_id,
            endpoint=faker.uri(),
            auth=faker.word(),
            p256dh=faker.word()
        )
        session.add(subscription)
    session.commit()

    # Create carts
    for user in users:
        cart = Cart(
            user_id=user.user_id,
            created_at=faker.date_this_year()
        )
        session.add(cart)
    session.commit()

    # Create cart items
    for cart in session.query(Cart).all():
        num_items = random.randint(1, 5)
        for _ in range(num_items):
            product = random.choice(products)
            cart_item = CartItem(
                cart_id=cart.cart_id,
                product_id=product.product_id,
                quantity=random.randint(1, 3)
            )
            session.add(cart_item)
    session.commit()


if __name__ == "__main__":
    
    engine = create_database()
    session = get_session(engine)
    populate_db(session)

    print("Data loading completed successfully!")
