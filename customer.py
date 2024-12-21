from datetime import datetime, timedelta, timezone
import random
from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required
import requests
from app import db
from models import Order, Audit, User, OrderItem, Subscription, Product, CartItem, Cart, Category


app = Blueprint("customer",__name__)

VAPID_PUBLIC_KEY = "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEvtwAO3smIZrG1ib6WhszNwnO+R8gMs8kVBymXXOnRUeNCmoddYdatn4FAbxvGh6LIka/8ERdL0C1e2g2BpGPXg=="

@app.route('/<int:order_id>/status', methods=['GET'])
@login_required
def status_update_timeline(order_id):
    customer_id = current_user.user_id
    if customer_id != Order.query.get(order_id).user_id:
        return jsonify({'error':'Unauthorized access, you do not have access'}), 403
    
    history = sorted(Audit.query.filter(Audit.order_id==order_id).all(), key=lambda x:x.updated_at)
    
    return render_template('status_update_timeline_t3.html', history=history)

@app.route('/service_worker')
def service_worker():
    response = send_from_directory(current_app.static_folder+'/js', 'service-worker.js')
    response.headers['Service-Worker-Allowed'] = '/' 
    return response

@app.route('/history', methods=['GET'])
@login_required
def history():
    customer_id = current_user.user_id
    customer = User.query.get(customer_id)
    if not customer or customer.role.lower() != 'customer':
        return jsonify({'error': 'Hello!, Please create an account'}), 404

    orders = sorted(Order.query.filter(Order.user_id==customer_id).all(), key=lambda x: x.created_at, reverse=True)
    orders_list = [{
        'order_id': order.order_id,
        'order_items': [item.product.name for item in OrderItem.query.filter(OrderItem.order_id==order.order_id).all()],
        'quantity': [str(item.quantity) for item in OrderItem.query.filter(OrderItem.order_id==order.order_id).all()],
        'price': float(order.total_price) + float(order.shipping_cost),
        'status': order.status,
        'estimated_delivery':order.estimated_delivery.strftime('%Y-%m-%d %H:%M:%S'),
        'customer_address': order.address+', '+str(order.pincode),
    } for order in orders]

    if request.args.get('json'):
        return jsonify({'orders': orders_list})

    return render_template('order_history_t3.html', orders=orders_list, customer_name=customer.name, customer_id=customer_id)

@app.route('/subscribe', methods=['POST'])
@login_required
def subscribe():
    data = request.json
    if not data or 'customer_id' not in data or 'subscription' not in data:
        return jsonify({'error': 'Invalid subscription data'}), 400

    customer_id = data['customer_id']
    subscription = data['subscription']

    try:
        # Check if subscription already exists
        existing_subscription = Subscription.query.filter_by(endpoint=subscription['endpoint']).first()

        if existing_subscription:
            # Update the existing subscription
            existing_subscription.user_id = customer_id
            existing_subscription.p256dh = subscription['keys']['p256dh']
            existing_subscription.auth = subscription['keys']['auth']
        else:
            # Add a new subscription
            new_subscription = Subscription(
                user_id=customer_id,
                endpoint=subscription['endpoint'],
                p256dh=subscription['keys']['p256dh'],
                auth=subscription['keys']['auth']
            )
            db.session.add(new_subscription)

        db.session.commit()
        return jsonify({'success': 'Subscription saved or updated!'}), 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({'error': f'Failed to save subscription: {str(e)}'}), 500
    


@app.route('/show_catalog', methods=['GET'])
def show_catalog():
    # products = Product.query.all()
    # return render_template("catalog_t2.html", products=products)
    category_name = request.args.get('category')
    search_query = request.args.get('search')
    sort_by = request.args.get('sort_by', 'name')

    products_query = Product.query

    if category_name:
        products_query = products_query.join(Category).filter(Category.category_name == category_name)

    if search_query:
        products_query = products_query.filter(
            Product.name.ilike(f"%{search_query}%") |
            Product.description.ilike(f"%{search_query}%")
        )

    if sort_by == 'price':
        products_query = products_query.order_by(Product.selling_price)
    elif sort_by == 'weight':
        products_query = products_query.order_by(Product.product_weight)
    else:
        products_query = products_query.order_by(Product.name)

    products = products_query.all()
    categories = Category.query.with_entities(Category.category_name).distinct()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check for AJAX
        return render_template('product_grid_t2.html', products=products)

    return render_template('products_t2.html', products=products, categories=categories, user=current_user)


@app.route('/show_products', methods=['GET'])
def show_products():
    category_name = request.args.get('category')
    search_query = request.args.get('search')
    sort_by = request.args.get('sort_by', 'name')

    products_query = Product.query

    if category_name:
        products_query = products_query.join(Category).filter(Category.category_name == category_name)

    if search_query:
        products_query = products_query.filter(
            Product.name.ilike(f"%{search_query}%") |
            Product.description.ilike(f"%{search_query}%")
        )

    if sort_by == 'price':
        products_query = products_query.order_by(Product.selling_price)
    elif sort_by == 'weight':
        products_query = products_query.order_by(Product.product_weight)
    else:
        products_query = products_query.order_by(Product.name)

    products = products_query.all()
    categories = Category.query.with_entities(Category.category_name).distinct()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check for AJAX
        return render_template('product_grid_t2.html', products=products)

    return render_template('products_t2.html', products=products, categories=categories, user=current_user)

@app.route('/product/<int:product_id>', methods=['GET'])
def product_details(product_id):
    product = Product.query.get_or_404(product_id)  # Fetch product by ID or return 404
    return render_template('product_details_t2.html', product=product, user=current_user)

def calculate_shipping_cost(pincode, total_weight, country):
    fixed_rate_for_outside_india = 500  # Fixed rate for countries outside India
    base_shipping_cost = 20  # Base cost for nearby locations

    # If the country is not India, return the fixed rate
    if country.lower() != 'india':
        return fixed_rate_for_outside_india

    # For locations within India, calculate cost based on distance using pincode
    outlet_pincode = '673001'  # Kozhikode, Kerala pincode

    # Using Google Maps Distance Matrix API
    try:
        api_key = "AIzaSyAv44pEZqLcd3Tck0ppI4TgTsAVetKeVfc"  
        response = requests.get(
            "https://maps.googleapis.com/maps/api/distancematrix/json",
            params={
                "origins": outlet_pincode,
                "destinations": pincode,
                "key": api_key,
            }
        )
        response.raise_for_status()
        distance_info = response.json()
        rows = distance_info.get('rows', [])
        elements = rows[0].get('elements', []) if rows else []
        distance = elements[0].get('distance', {}).get('value', 0) / 1000  # Convert meters to kilometers
    except Exception as e:
        flash(f"Could not calculate shipping cost: {e}", 'warning')
        return base_shipping_cost  # Fallback to base cost

    # Distance-based charges
    if distance <= 200:
        distance_cost = 20  # Nearby locations
    elif distance <= 500:
        distance_cost = 50  # Medium range
    else:
        distance_cost = 100  # Long-distance

    # Weight-based charges
    if total_weight <= 2:
        weight_cost = 20  # Flat rate for up to 2 kg
    else:
        weight_cost = 20 + (10 * (total_weight - 2))  # ₹10 per kg for additional weight

    # Calculate total shipping cost
    shipping_cost = base_shipping_cost + weight_cost + distance_cost
    return shipping_cost


@app.route('/cust_profile', methods=['GET', 'POST'])
@login_required
def cust_profile():
    if request.method == 'POST':
        recipient_name = request.form.get('recipient_name')
        address = request.form.get('address')
        pin = request.form.get('pin')
        phone_no = request.form.get('phone_no')

        current_user.name = recipient_name
        current_user.phone_number = phone_no
        current_user.address = address
        current_user.pincode = pin
        db.session.commit()

        flash("Profile updated successfully!", "success")
        return redirect(url_for('customer.cust_profile'))

    return render_template('cust_profile_t1.html', user=current_user)

@app.route('/view_cart')
@login_required
def view_cart():
    if current_user.role != 'customer':
        return jsonify({'error':'Only customers are allowed to view cart'})
    cart = Cart.query.filter_by(user_id=current_user.user_id).first()
    if not cart or not cart.cart_items:
        flash('Your cart is empty.', 'info')
        return redirect(url_for('customer.show_products'))

    cart_items = CartItem.query.filter_by(cart_id=cart.cart_id).all()
    total_price = sum(item.quantity * item.product.selling_price for item in cart_items)
    total_weight = sum(item.product.product_weight * item.quantity for item in cart_items)

    if not current_user.country:
        flash('Please update country and try again')
        return redirect(url_for('customer.cust_profile'))

    try:
        total_shipping_cost = calculate_shipping_cost(
            pincode=current_user.pincode,
            total_weight=total_weight,
            country=current_user.country
        )
    except Exception as e:
        flash("Shipping cost could not be calculated. Please check your details.", "danger")
        total_shipping_cost = 0

    # Total price including shipping
    total_price_with_shipping = total_price + total_shipping_cost

    return render_template('cart_t2.html',user=current_user, cart_items=cart_items, total_price=total_price,
                            total_weight=total_weight,shipping_cost=total_shipping_cost,
                            total_price_with_shipping=total_price_with_shipping)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    if current_user.role != 'customer':
        return jsonify({'error':'only customers can add products to cart'})
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get("quantity"))
    cart = Cart.query.filter_by(user_id=current_user.user_id).first()
    if not cart:
        cart = Cart(user_id=current_user.user_id)
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem.query.filter_by(cart_id=cart.cart_id, product_id=product.product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.cart_id, product_id=product.product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    flash(f'{product.name} added to cart!', 'success')
    return redirect(url_for('customer.show_products'))

@app.route('/update_cart/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.cart.user_id != current_user.user_id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('customer.view_cart'))

    try:
        new_quantity = int(request.form.get('quantity', 1))
        if new_quantity < 1:
            db.session.delete(cart_item)
            message = "Item removed from cart."
        else:
            cart_item.quantity = new_quantity
            message = "Cart updated."

        db.session.commit()
        return jsonify({"success": True, "message": message})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.cart.user_id != current_user.user_id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('customer.view_cart'))

    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart.', 'info')
    return redirect(url_for('customer.view_cart'))


@app.route('/cart_summary', methods=['POST'])
@login_required
def cart_summary():
    cart = Cart.query.filter_by(user_id=current_user.user_id).first()
    if not cart or not cart.cart_items:
        return jsonify({'success': False, 'error': 'Cart is empty.'}), 400

    cart_items = CartItem.query.filter_by(cart_id=cart.cart_id).all()

    # Calculate total price and weight
    total_price = sum(item.quantity * item.product.selling_price for item in cart_items)
    total_weight = sum(item.product.product_weight * item.quantity for item in cart_items)

    # Calculate shipping cost
    try:
        shipping_cost = calculate_shipping_cost(
            pincode=current_user.pincode,
            total_weight=total_weight,
            country=current_user.country
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

    # Calculate total price with shipping
    total_price_with_shipping = total_price + shipping_cost

    return jsonify({
        'success': True,
        'subtotal': round(total_price, 2),
        'total_weight': round(total_weight, 2),
        'shipping_cost': round(shipping_cost, 2),
        'total_price_with_shipping': round(total_price_with_shipping, 2),
    })


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = Cart.query.filter_by(user_id=current_user.user_id).first()
    if not cart or not cart.cart_items:
        flash('Your cart is empty. Add some products before checking out.', 'info')
        return redirect(url_for('customer.show_products'))
    if not current_user.address or not current_user.pincode:
        flash('Address and Pincode are required to Place Order. Please update details.','warning')
        return redirect(url_for('customer.cust_profile'))
    for cart_item in cart.cart_items:
        product = cart_item.product
        # Check stock availability
        if cart_item.quantity > product.stock_quantity:
            flash(f"Insufficient stock for {product.name}. Reduce the quantity and try again.", "warning")
            db.session.rollback()
            return redirect(url_for('customer.view_cart'))
        
    total_weight = sum(item.product.product_weight * item.quantity for item in cart.cart_items)

    # Calculate shipping cost based on total weight
    shipping_cost = calculate_shipping_cost(
        pincode=current_user.pincode,
        total_weight=total_weight,
        country=current_user.country
    )

    # Create the order
    total_price = sum(item.quantity * item.product.selling_price for item in cart.cart_items)
    order = Order(user_id=current_user.user_id, total_price=total_price, status='Processing',address=current_user.address, pincode=current_user.pincode,shipping_cost=shipping_cost,
                  assigned_to=random.choice([courier_id[0] for courier_id in User.query.with_entities(User.user_id).filter(User.role=='courier_service_provider').all()]),
                  estimated_delivery=(datetime.now(timezone.utc)+timedelta(days=random.randint(5,10))).replace(hour=21,minute=0,second=0,microsecond=0))
    db.session.add(order)
    db.session.commit()

    # Add items to the order
    for cart_item in cart.cart_items:
        # Reduce stock quantity
        product.stock_quantity -= cart_item.quantity
        if product.stock_quantity == 0:
            # Remove product record from the database
            db.session.delete(product)
            flash(f"The product '{product.name}' is now out of stock and has been removed.", "info")

        order_item = OrderItem(
            order_id=order.order_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )
        audit_log = Audit(
            order_id=order.order_id,
            status=order.status,
            updated_by=order.assigned_to,
            reason='Order has been Placed and is under process.'
        )
        db.session.add(audit_log)
        db.session.add(order_item)
        db.session.delete(cart_item)  # Remove the item from the cart

    # Empty the cart after checkout
    db.session.commit()

    flash('Your order has been placed successfully!', 'success')
    return redirect(url_for('customer.order_summary', order_id=order.order_id))


@app.route('/order/<int:order_id>')
@login_required
def order_summary(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.user_id:
        flash('Unauthorized access to this order.', 'danger')
        return redirect(url_for('customer.show_products'))

    return render_template('order_summary_t2.html', order=order)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Handle contact form submission
        flash(f"Thank you {name}, we have received your message!", "success")
        return redirect(url_for('customer.contact'))
    return render_template('contact_t1.html')


if __name__ == '__main__':
    app.run(debug=True)