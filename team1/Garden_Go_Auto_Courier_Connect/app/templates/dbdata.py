from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Create a new user, leaving created_at as None (NULL)
    new_user = User(
        name="john_doe",
        email="john@example.com",
        phone="1234567890",
        shipping_address={"city": "City", "door_no": "123", "street": "Street", "state": "State", "zipcode": "12345"},
        role="customer",
        token_id=None,
        profile_update_at=None,
        created_at=None,  # This can be set to None (which is NULL in the database)
        last_login=None
    )
    db.session.add(new_user)
    db.session.commit()

    print("User added successfully!")
