import pytest
from app import create_app

# Fixture to create an app instance for testing
@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app

# Fixture to create a test client for the app
@pytest.fixture
def client(app):
    return app.test_client()

# Test total sales endpoint
def test_total_sales(client):
    response = client.get('/api/total_sales')
    assert response.status_code == 200
    data = response.get_json()
    assert "total_sales" in data

# Test total profit endpoint
def test_total_profit(client):
    response = client.get('/api/total_profit')
    assert response.status_code == 200
    data = response.get_json()
    assert "total_profit" in data

# Test average order price endpoint
def test_average_order_price(client):
    response = client.get('/api/average_order_price')
    assert response.status_code == 200
    data = response.get_json()
    assert "average_order_price" in data

# Test total sales by category endpoint
def test_total_sales_by_category(client):
    response = client.get('/api/total_sales_by_category')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# Test product availability endpoint
def test_product_availability(client):
    response = client.get('/api/product_availability')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# Test daily profit endpoint
def test_daily_profit(client):
    response = client.get('/api/daily_profit')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# Test daily sales endpoint
def test_daily_sales(client):
    response = client.get('/api/daily_sales')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# Test top performing products endpoint
def test_top_performing_products(client):
    response = client.get('/api/top_performing_products')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# Test sales for a filtered season endpoint
def test_sales_for_filtered_season(client):
    response = client.get('/api/sales/season?season=summer')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# Test customer count by location endpoint
def test_customer_count_by_location(client):
    response = client.get('/api/customers/location?location=country')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# Test repeat customer rate endpoint
def test_repeat_customer_rate(client):
    response = client.get('/api/repeat_customer_rate')
    assert response.status_code == 200
    data = response.get_json()
    assert "repeat_customer_rate" in data

# Test monthly customer counts endpoint
def test_monthly_customer_counts(client):
    response = client.get('/api/monthly_customer_counts')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# Test delivery performance endpoint
def test_delivery_performance(client):
    response = client.get('/api/delivery_performance')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
