from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker 
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__, template_folder='templates')


go = declarative_base()   #base class declaration 

Database_URl = 'sqlite:///garden.db'        #db url 
engine = create_engine(Database_URl)        #creating engine 
Session = sessionmaker(bind=engine)         # creating session 


#creating category table 
class Category(go): 
    __tablename__ ='category'

    category_Id = Column(Integer, primary_key= True, autoincrement=True)
    category_Name = Column(String(50), nullable=False)
    category_description = Column(Text)

    products = relationship("Product", backref="category")

#creating product table 
class Product(go):
    __tablename__ = 'product'

    product_Id = Column(Integer, primary_key=True, autoincrement=True)
    product_Name =  Column(String(100), nullable=False)
    product_Description =  Column(Text)
    product_Price = Column(Integer, nullable=False)
    category_Id = Column(Integer, ForeignKey(Category.category_Id))
    product_Image_Url = Column(Text, nullable=False)
    stock_Quatity = Column(Integer, default = 0)

    inventories = relationship("Inventory", backref= "product")
    order_items = relationship("Order_Item", backref="product")

#creating order item table 
class Order_Item(go):
    __tablename__= 'order_Item'

    order_Item_Id = Column(Integer, primary_key=True, autoincrement=True)
    product_Id = Column(Integer, ForeignKey(Product.product_Id))
    # order_Id = Column(Integer, ForeignKey(order.order_Id))
    product_Price = Column(Integer, nullable=False)


#creating inventory table 
class Inventory(go):
    __tablename__ = 'inventory'
    
    inventory_Id = Column(Integer, primary_key=True, autoincrement=True)
    product_Id = Column(Integer, ForeignKey(Product.product_Id))
    quantity_Available = Column(Integer, default=0)
    # warehouse_Location = Column(Text, nullable=False)



go.metadata.create_all(engine)      #it create tables and schemas defined above 

@app.route('/')
def index():
    session = Session()
    products = session.query(Product).all()
    session.close()
    return render_template('index.html', products = products)

@app.route('/add_product', methods = ['POST'])              #for adding product from html page  to product and inventory table 
def add_product():
    if request.method == 'POST':
        session = Session()
        new_products = Product(
            product_Name = request.form['name'],
            product_Description = request.form['description'],
            product_Price = request.form['price'],
            product_Image_Url=request.form['image_url'],
            stock_Quatity=request.form['stock_quantity'],

            #category'
        )
        session.add(new_products)
        session.commit()
        new_Inventory = Inventory(
            inventory_Id = new_products.product_Id,
            quantity_Available = new_products.stock_Quatity
        )
        session.add(new_Inventory)
        session.commit()
        session.close()
        return redirect(url_for('index'))
    return render_template('add_products.html')

@app.route('/edit_product/<int:product_Id>', methods = ['GET', 'POST'])         #for editing products from html page from product and inventory table
def edit_product(product_Id):
    session = Session()
    product = Product.query.get_or_404(product_Id)
    if request.method == 'POST':
        product.product_Name = request.form['name'],
        product.product_Description = request.form['description'],
        product.product_Price = request.form['price'],
        product.product_Image_Url = request.form['image_url']
    
        inventory = Inventory.query.filter_by(product_Id = product_Id).first()
        if inventory:
            inventory.stock_quantity = request.form['quantity']

        session.commit()

        return redirect(url_for('index'))
    return render_template('edit_product.html', product = product)

@app.route('/delete_product/<int:product_Id>', methods = ['POST'])                  #for deleting products from html page from product and inventory table
def delete_product(product_Id):
    session = Session()
    product = Session.query(Product).get(product_Id)
    if request.method == 'POST':
        if product:
            inventory = Inventory.query.filter_by(product_Id = product_Id).first()
            if inventory:
                Session.delete(inventory)
            Session.delete(product)
            Session.commit()
        return redirect(url_for('index'))
    return render_template('delete_product.html', product = product)

@app.route('/view_product/<int:product_Id>', methods = ['GET'])                 #for viewing products from html page from product and inventory table
def view_Product(product_Id):
    product = Session.query(Product).get(product_Id)

    if product:
        return render_template('view_product', product = product)


if __name__ == '__main__':

    app.run(debug = True) 