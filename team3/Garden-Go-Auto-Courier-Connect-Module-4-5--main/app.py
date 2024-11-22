from datetime import datetime, timezone
from flask import Flask, jsonify, redirect, render_template, request, url_for
from models import db, Courier, Order, Audit

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courier_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/courier/<int:courier_id>/orders', methods=['GET'])
def get_assigned_orders(courier_id):
    courier = Courier.query.get(courier_id)
    if not courier:
        return jsonify({'error': 'Courier not found'}), 404

    orders = Order.query.filter(Order.courier_id==courier_id, Order.status != "Delivered").all()
    orders_list = [{
        'order_id': order.order_id,
        'customer_name': order.customer_name,
        'customer_address': order.customer_address+', '+str(order.pincode),
        'customer_phone': order.customer_phone,
        'products': synthetic_order_list.get(order.order_id),
        'quantity': synthetic_quantity.get(order.order_id),
        'status': order.status,
        'estimated_delivery':order.estimated_delivery.strftime('%Y-%m-%d'),
        'created_at': order.created_at,
        'updated_at': order.updated_at
    } for order in orders]

    if request.args.get('json'):
        return jsonify({'orders': orders_list})

    return render_template('index.html', orders=orders_list, courier_id=courier_id)

@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    order_id = request.form.get('order_id')
    new_status = request.form.get('new_status')
    reason = request.form.get('reason')
    updated_by = request.form.get('courier_id')

    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    print(updated_by)
    print(new_status)

    log_audit_entry(order_id, new_status, updated_by, reason)

    order.status = new_status
    order.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return redirect(url_for('get_assigned_orders', courier_id=order.courier_id))

def log_audit_entry(order_id, new_status, updated_by, reason=None):
    """Function to log audit entries when order status changes."""
    audit_entry = Audit(
        order_id=order_id,
        status=new_status,
        updated_at=datetime.now(timezone.utc),
        updated_by=updated_by,
        reason=reason
    )
    print(updated_by)
    db.session.add(audit_entry)
    db.session.commit()

synthetic_order_list ={1:"Aloe Vera Plant",2:"Rosemary Plant",3:"Basil Plant",4:"Peace Lily Plant",
                       5:"Lavender Plant", 6:"Aloe Vera Plant",7:"Lavender Plant",8:"Sunflower Seeds",
                       9:"Pumpkin Seeds", 10:"Rosemary Plant", 11:"Basil Plant",12:"Sunflower Seeds",
                       13:"Watermelon Seeds",14:"Rice Seeds",15:"Wheat Seeds",16:"Tomato Seeds",
                       17:"Basil Plant",18:"Cumin Seeds",19:"Pumpkin Seeds",20:"Sunflower Seeds",
                       21:"Coriander Seeds",22:"Tomato Seeds",23:"Carrot Seeds",24:"Rice Seeds",25:"Wheat Seeds"}

synthetic_quantity = {1:3,2:5,3:6,4:1,5:3,6:2,7:5,8:5,9:3,10:3,11:4,12:5,13:7,14:8,15:4,16:4,17:5,18:6,
                      19:7,20:5,21:3,22:7,23:8,24:6,25:5}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
