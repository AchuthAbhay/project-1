import requests

base_url = "http://127.0.0.1:5000/"
 
def total_sales():
    url = f"{base_url}/api/top_performing_products"
    data = requests.get(url)
    print(data.status_code, data.json())
    

total_sales()