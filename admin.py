from flask import Blueprint, flash, jsonify, redirect, render_template, request, send_from_directory, url_for
from app import db
from models import Product,Category
from flask_login import current_user, login_required


app = Blueprint("admin",__name__)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    categories = db.session.query(Category).all()
    products_by_category = {}

    for category in categories:
        products_by_category[category] = db.session.query(Product).filter_by(category_id=category.category_id).all()

    return render_template('admin_dashboard_t1.html', user=current_user,categories=categories, products_by_category=products_by_category)


@app.route('/admin_summary')
@login_required
def admin_summary():
    return render_template('admin_summary_t1.html', user=current_user)


@app.route('/add_pro', methods=['GET', 'POST'])
@login_required
def add_pro():
    if request.method == 'POST':
        product_name = request.form['name']
        product_category = request.form['category']
        cost_price = request.form['cost_price']
        selling_price = request.form['selling_price']
        product_image = request.form['image_url']
        stock_quantity = request.form['quantity']
        product_description = request.form['description']
        
        new_product = Product(
            name=product_name,
            category_id=product_category,
            cost_price=cost_price,
            selling_price=selling_price,
            stock_quantity=stock_quantity,
            image_url=product_image,
            description=product_description
        )
        
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('admin.admin_dashboard'))  # Redirect to the dashboard after adding a product

    categories = db.session.query(Category).all()  # Fetch all categories for the form
    return render_template('add_pro_form_t2.html', categories=categories,user=current_user)  # Return the template with categories

@app.route('/edit_product/', methods=['POST'])
@login_required
def edit_product():
    product_id = int(request.form.get('product_id'))
    product = Product.query.get(product_id)
    if not product:
        return "Product not found", 404

    categories = db.session.query(Category).all() 
    if request.method == 'POST' and request.form.get('action') == 'update':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.cost_price = request.form.get('cost_price')
        product.selling_price = request.form.get('selling_price')
        product.quantity = request.form.get('quantity')
        product.category_id = request.form.get('category')
        product.image_url = request.form.get('image_url')
        db.session.commit()
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('edit_product_t2.html', product=product, categories=categories)  

@app.route('/delete_product', methods=['POST'])
@login_required
def delete_product():
    """Delete a product."""
    product_id = int(request.form.get("product_id"))
    product = Product.query.get(product_id)
    if not product:
        return "Product not found", 404
    if request.method == 'POST' and request.form.get('action') == 'delete':
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('delete_product_t2.html', product_id=product_id)