import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from app import db
from models import Product,Category
from flask_login import current_user, login_required


app = Blueprint("admin",__name__)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    categories = db.session.query(Category).all()
    products_by_category = {}

    search_query = request.args.get('search')

    products_query = Product.query

    if search_query:
        products_query = products_query.filter(
            Product.name.ilike(f"%{search_query}%") |
            Product.description.ilike(f"%{search_query}%")
        )

    products = products_query.all()
    

    for category in categories:
        products_by_category[category] = [product for product in products if product.category_id == category.category_id]

    return render_template('admin_dashboard_t1.html', user=current_user,categories=categories, products_by_category=products_by_category)



@app.route('/add_pro', methods=['GET', 'POST'])
@login_required
def add_pro():
    if request.method == 'POST':
        product_name = request.form['name']
        product_category = request.form['category']
        cost_price = request.form['cost_price']
        selling_price = request.form['selling_price']
        stock_quantity = request.form['quantity']
        product_description = request.form['description']
        product_weight = request.form['weight']

        image_option = request.form.get('image_option')
        image_url = None

        if image_option == 'url':
            image_url = request.form['image_url']
        elif image_option == 'file' and 'image_file' in request.files:
            image_file = request.files['image_file']
            image_path = os.path.join('static/uploads', image_file.filename)
            image_file.save(image_path)
            print(image_path)
            image_url = image_path
            print(image_url)
        else:
            flash('Error while uploading image','error')
            return redirect(url_for('admin.add_pro'))
        
        new_product = Product(
            name=product_name,
            category_id=product_category,
            cost_price=cost_price,
            selling_price=selling_price,
            stock_quantity=stock_quantity,
            image_url=image_url,
            description=product_description,
            product_weight = product_weight
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
        product.stock_quantity = request.form.get('quantity')
        product.category_id = request.form.get('category')
        product.product_weight = request.form.get('weight')

        image_option = request.form.get('image_option')
        if image_option == 'url':
            product.image_url = request.form['image_url']
        elif image_option == 'file' and 'image_file' in request.files:
            image_file = request.files['image_file']
            if image_file.filename != '':
                image_path = os.path.join('static/uploads', image_file.filename)
                image_file.save(image_path)
                product.image_url = image_path

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