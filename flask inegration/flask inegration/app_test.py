import requests

base_url = "http://127.0.0.1:5000/"
 
def test_total_sales():
    url = f"{base_url}/api/total_sales"
    data = requests.get(url)
    assert data.status_code==200
    assert 'category' in data.json()[0]
    assert 'product' in data.json()[0]
    assert 'total_sales' in data.json()[0]
    
def test_total_sales_by_category():
    url = f"{base_url}/api/total_sales_by_category"
    data = requests.get(url)
    assert data.status_code==200
    assert 'category' in data.json()[0]
    assert 'total_sales' in data.json()[0]
    
def test_product_availability():
    url = f"{base_url}/api/product_availability"
    data = requests.get(url)
    assert data.status_code==200
    assert 'availability_count' in data.json()[0]
    assert 'product' in data.json()[0]
    
def test_daily_profit():
    url = f"{base_url}/api/daily_profit"
    data = requests.get(url)
    assert data.status_code==200
    assert 'daily_profit' in data.json()[0]
    assert 'date' in data.json()[0]
   
def test_daily_sales():
    url = f"{base_url}/api/daily_sales"
    data = requests.get(url)
    assert data.status_code==200
    assert 'sale_date' in data.json()[0]
    assert 'total_sales' in data.json()[0]
    
def test_top_performing_products():
    url = f"{base_url}/api/top_performing_products"
    data = requests.get(url)
    assert data.status_code==200
    assert 'product_name' in data.json()[0]
    assert 'total_sales' in data.json()[0]