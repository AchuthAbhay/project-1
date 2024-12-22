import requests

# Base URL for the Flask app
base_url = "http://127.0.0.1:5000"

# Login credentials for testing
test_email = "admin1@gmail.com"
test_password = "admin1"

# Global variable for authentication cookies or token
auth_cookies = None
auth_headers = None


def test_login():
    """Authenticate and retrieve cookies or tokens for API requests."""
    global auth_cookies, auth_headers

    # Login endpoint
    url = f"{base_url}/auth"
    data = {"email": test_email, "password": test_password}

    # Send login request
    response = requests.post(url, data=data)

    # Check login success
    if response.status_code == 200:
        # Use cookies for session-based authentication
        auth_cookies = response.cookies

        # If using token-based authentication, set token header
        try:
            token = response.json().get("token")
            if token:
                auth_headers = {"Authorization": f"Bearer {token}"}
        except ValueError:
            pass
    else:
        raise Exception(f"Login failed: {response.status_code} {response.text}")


def validate_response(data, status_code=200, keys=None):
    """Helper function to validate API responses."""
    assert data.status_code == status_code, f"Unexpected status code: {data.status_code}"
    try:
        json_data = data.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    assert json_data, "Response is empty"

    if keys:
        if isinstance(json_data, dict):
            # Check keys in a dictionary
            for key in keys:
                assert key in json_data, f"Missing key in response: {key}"
        elif isinstance(json_data, list):
            # Check keys in the first element of a list
            for key in keys:
                assert key in json_data[0], f"Missing key in response: {key}"
        else:
            assert False, "Response JSON is not a dictionary or list"


# Test functions
def test_total_sales():
    url = f"{base_url}/api/total_sales"
    response = requests.get(url, cookies=auth_cookies, headers=auth_headers)
    validate_response(response, keys=["total_sales"])


def test_total_sales_by_category():
    url = f"{base_url}/api/total_sales_by_category"
    response = requests.get(url, cookies=auth_cookies, headers=auth_headers)
    validate_response(response, keys=["category", "total_sales"])


def test_product_availability():
    url = f"{base_url}/api/product_availability"
    response = requests.get(url, cookies=auth_cookies, headers=auth_headers)
    validate_response(response, keys=["product", "availability_count"])


def test_daily_profit():
    url = f"{base_url}/api/daily_profit"
    response = requests.get(url, cookies=auth_cookies, headers=auth_headers)
    validate_response(response, keys=["date", "daily_profit"])


def test_daily_sales():
    url = f"{base_url}/api/daily_sales"
    response = requests.get(url, cookies=auth_cookies, headers=auth_headers)
    validate_response(response, keys=["sale_date", "total_sales"])


def test_top_performing_products():
    url = f"{base_url}/api/top_performing_products"
    response = requests.get(url, cookies=auth_cookies, headers=auth_headers)
    validate_response(response, keys=["product_name", "total_sales"])


def test_sales_for_filtered_season():
    url = f"{base_url}/api/sales/season"
    params = {"season": "summer"}
    response = requests.get(url, params=params, cookies=auth_cookies, headers=auth_headers)
    validate_response(response, keys=["product_name", "total_sales"])


def test_customer_count_by_location():
    url = f"{base_url}/api/customers/location"
    params = {"location": "country"}
    response = requests.get(url, params=params, cookies=auth_cookies, headers=auth_headers)
    validate_response(response, keys=["location", "user_count"])


def test_repeat_customer_rate():
    url = f"{base_url}/api/repeat_customer_rate"
    response = requests.get(url, cookies=auth_cookies, headers=auth_headers)
    validate_response(response, keys=["repeat_customer_rate"])


def test_delivery_performance():
    url = f"{base_url}/api/delivery_performance"
    response = requests.get(url, cookies=auth_cookies, headers=auth_headers)
    validate_response(response, keys=["delivery_type", "count"])


# Run all tests
if __name__ == "__main__":
    try:
        # Authenticate before running tests
        test_login()

        # Run tests
        test_total_sales()
        test_total_sales_by_category()
        test_product_availability()
        test_daily_profit()
        test_daily_sales()
        test_top_performing_products()
        test_sales_for_filtered_season()
        test_customer_count_by_location()
        test_repeat_customer_rate()
        test_delivery_performance()
        print("All 10 tests passed!")
    except Exception as e:
        print(f"Test failed: {e}")
