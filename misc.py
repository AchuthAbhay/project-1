from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

app = Blueprint("misc",__name__)

@app.route('/track_order', methods=['GET', 'POST'])
@login_required
def track_order():
    if request.method == 'POST':
        # Logic to track the order
        order_id = request.form.get('order_id')
        flash(f"Order {order_id} status: In transit", "info")
        return redirect(url_for('track_order'))
    return render_template('track_order.html')

# @app.route('/products', methods=['GET'])
# def products():
#     # Logic to fetch product data
#     products = [{"name": "Rose Plant", "price": "$10"}, {"name": "Gardening Tool Kit", "price": "$25"}]
#     return render_template('products.html', products=products)

@app.route('/profile_completion')
@login_required
def profile_completion():
    return render_template('profile_completion.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Handle contact form submission
        flash(f"Thank you {name}, we have received your message!", "success")
        return redirect(url_for('contact'))
    return render_template('contact.html')