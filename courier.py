from datetime import datetime, timezone
from flask import Blueprint, flash, json, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app import db
from models import Order, Audit, User, OrderItem, Subscription
from pywebpush import webpush, WebPushException

app = Blueprint("courier", __name__)

@app.route('/courier_dashboard')
@login_required
def courier_dashboard():
    courier_id = current_user.user_id
    courier = User.query.get(courier_id)
    if not courier or courier.role != 'courier_service_provider':
        return jsonify({'error': 'Courier not found'}), 404

    orders = Order.query.filter(Order.assigned_to==courier_id, Order.status != "Delivered").all()
    orders_list = [{
        'order_id': order.order_id,
        'customer_name': User.query.get(order.user_id).name,
        'customer_address': order.address+', '+str(order.pincode),
        'customer_phone': User.query.get(order.user_id).phone_number,
        'products': [item.product.name if item.product else 'Unknown Product' for item in OrderItem.query.filter(OrderItem.order_id==order.order_id).all()],
        'quantity': [str(item.quantity) for item in OrderItem.query.filter(OrderItem.order_id==order.order_id).all()],
        'status': order.status,
        'estimated_delivery':order.estimated_delivery.strftime('%Y-%m-%d %H:%M:%S'),
        'created_at': order.created_at,
        'updated_at': order.updated_at
    } for order in orders]

    if request.args.get('json'):
        return jsonify({'orders': orders_list})

    return render_template('courier_dashboard_t3.html', orders=orders_list, courier_id=courier_id)


@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    updated_by = int(request.form.get('courier_id'))
    if updated_by != current_user.user_id:
        return jsonify({'error':'Unauthorized'}), 401
    order_id = request.form.get('order_id')
    new_status = request.form.get('new_status')
    msg = request.form.get('reason')

    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    log_audit_entry(order_id, new_status, updated_by, msg)

    order.status = new_status
    order.updated_at = datetime.now(timezone.utc)
    if new_status == 'Delivered':
        order.actual_delivery = order.updated_at
    db.session.commit()

    subscriptions = Subscription.query.filter_by(user_id=order.user_id).all()
    for sub in subscriptions:
        send_push_notification(
            sub.endpoint,
            sub.p256dh,
            sub.auth,
            {'title':'Order Status Update',
            'body':f"Your order {order_id} status has been updated to {new_status}.",
            'url':f"/{order_id}/status"}
        )

    return redirect(url_for('courier.courier_dashboard'))

def log_audit_entry(order_id, new_status, updated_by, reason=None):
    """Function to log audit entries when order status changes."""
    if reason != None:
        msg = reason
    elif new_status == 'Processing':
        msg = "Order has been Placed and is under process"
    elif new_status=='Picked Up':
        msg = "Order has been picked up by the courier."
    elif new_status=='In Transit':
        msg = 'The package is on its way.' 
    elif new_status=='Out For Delivery':
        msg = 'The package is out for delivery.'
    elif new_status=='Delivered':
        msg = 'The package has been delivered to the customer.'
    else:
        msg = ''
    audit_entry = Audit(
        order_id=order_id,
        status=new_status,
        updated_at=datetime.now(timezone.utc),
        updated_by=updated_by,
        reason=msg
    )
    print(updated_by)
    db.session.add(audit_entry)
    db.session.commit()

VAPID_PRIVATE_KEY = 'MHcCAQEEICyRrCC0HK4f74Y3feLpPR3Lree44OXlB+KnVWnGpcxfoAoGCCqGSM49AwEHoUQDQgAEHBq85ZZuWr2tfp9qp40B0RdFZ9pEPStguAkwIwZxjRJIUdBgOEbsPr1wCMebdEsveFLE++w90FkCpCgyZsRiPw=='

def send_push_notification(endpoint, p256dh, auth, message):
    try:
        webpush(
            subscription_info={
                "endpoint": endpoint,
                "keys": {
                    "p256dh": p256dh,
                    "auth": auth
                }
            },
            data=json.dumps(message),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={
                "sub": "mailto:rohith832860@gmail.com"
            }
        )
    except WebPushException as ex:
        print(f"Failed to send push notification: {ex}")



@app.route('/courier_summary')
@login_required
def courier_summary():
    courier_id = current_user.user_id
    courier = User.query.get(courier_id)
    if not courier or courier.role != 'courier_service_provider':
        return jsonify({'error': 'Courier not found'}), 404

    orders = Order.query.filter(Order.assigned_to==courier_id, Order.status == "Delivered").all()
    orders_list = [{
        'order_id': order.order_id,
        'customer_name': order.user.name,
        'customer_address': order.address+', '+str(order.pincode),
        'customer_phone': order.user.phone_number,
        'products': '\n'.join([item.product.name if item.product else 'Unknown Product' for item in OrderItem.query.filter(OrderItem.order_id==order.order_id).all()]),
        'quantity': '\n'.join([str(item.quantity) for item in OrderItem.query.filter(OrderItem.order_id==order.order_id).all()]),
        'delivered_at':order.actual_delivery.strftime('%Y-%m-%d %H:%M:%S'),
    } for order in orders]
    return render_template('courier_summary_t1.html',orders=orders_list, user_name=current_user.name)


@app.route('/courier_profile', methods=['GET', 'POST'])
@login_required
def courier_profile():
    if request.method == 'POST':
        # Get courier-specific data
        phone_no = request.form.get('phone_no')
        vehicle_info = request.form.get('vehicle_info')
        vehicle_no = request.form.get('vehicle_no')

        # Update user profile
        current_user.phone_number = phone_no
        current_user.vehicle_info = vehicle_info
        current_user.vehicle_number = vehicle_no
        db.session.commit()
        
        flash("Profile updated successfully!", "success")
        return redirect(url_for('courier.courier_profile'))

    return render_template('courier_profile_t1.html', user=current_user)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)