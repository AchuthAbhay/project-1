import unittest
from app import app, db
from models import Courier, Order, Audit

class CourierAppTestCase(unittest.TestCase):
    # This function sets up a test environment before each test case.
    def setUp(self):
        self.app = app.test_client()  # Initialize test client for Flask app
        self.app.testing = True  # Enable testing mode
        
        with app.app_context():
            # Create all database tables for testing
            db.create_all()
            
            # Add a sample courier to the database
            courier = Courier(name='Test Courier', phone_no='1234567890')
            db.session.add(courier)
            db.session.commit()
            
            # Add a sample order assigned to the test courier
            order = Order(
                customer_name='John Doe', 
                customer_address='123 Test St', 
                customer_phone='9876543210', 
                pincode=123456,
                courier_id=courier.courier_id,  # Associate the order with the created courier
                status='Pending'
            )
            db.session.add(order)
            db.session.commit()

            # Save IDs for use in test cases
            self.courier_id = courier.courier_id
            self.order_id = order.order_id

    # This function cleans up the database after each test case.
    def tearDown(self):
        with app.app_context():
            db.session.remove()  # Remove session to prevent conflicts
            db.drop_all()  # Drop all tables to reset the database

    # Test the endpoint that retrieves all orders assigned to a courier.
    def test_get_assigned_orders(self):
        # Send GET request to retrieve orders assigned to the test courier
        response = self.app.get(f'/courier/{self.courier_id}/orders?json=true')
        
        # Check the response status code to confirm successful API call
        self.assertEqual(response.status_code, 200)
        
        # Parse the response as JSON and validate its structure
        response_json = response.get_json()  # Extract JSON from response
        self.assertIsNotNone(response_json)  # Ensure the response is not None
        self.assertIn('orders', response_json)  # Verify the 'orders' key exists

        # Error case: Invalid courier ID
        invalid_courier_id = 9999
        response = self.app.get(f'/courier/{invalid_courier_id}/orders?json=true')
        self.assertEqual(response.status_code, 404)  # Not Found

    # Test the functionality to update the status of an order.
    def test_update_order_status(self):
        # Define the new status and reason for the update
        new_status = 'Delivered'
        reason = 'Customer received the package'
        
        # Send POST request to update the order status
        response = self.app.post('/update_order_status', data={
            'order_id': self.order_id,
            'new_status': new_status,
            'reason': reason,
            'courier_id': self.courier_id
        })
        
        # Check if the request resulted in a redirect (302 status code)
        self.assertEqual(response.status_code, 302)
        
        # Verify the order's status is updated in the database
        with app.app_context():
            order = Order.query.get(self.order_id)  # Fetch the order by ID
            self.assertEqual(order.status, new_status)  # Check if the status matches the new value
        
        # Verify an audit entry is created in the database
        with app.app_context():
            audit_entry = Audit.query.filter_by(order_id=self.order_id).first()
            self.assertIsNotNone(audit_entry)  # Ensure an audit entry exists
            self.assertEqual(audit_entry.status, new_status)  # Check the audit status matches

    def test_get_assigned_orders_json(self):
        """
        Purpose:
        Test the JSON response of the 'get assigned orders' API endpoint.
        - Ensures the endpoint returns a successful HTTP response.
        - Confirms the response JSON contains the expected 'orders' data.
        """
        # Send GET request to fetch assigned orders in JSON format
        response = self.app.get(f'/courier/{self.courier_id}/orders?json=true')
        
        # Validate the response status code
        self.assertEqual(response.status_code, 200)
        
        # Parse and validate the response JSON
        response_json = response.get_json()  # Extract JSON from response
        self.assertIsNotNone(response_json)  # Ensure the response is not None
        self.assertIn('orders', response_json)  # Verify 'orders' key exists in the response

if __name__ == '__main__':
    unittest.main()

