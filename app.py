from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from itsdangerous import URLSafeTimedSerializer
from flask_cors import CORS
import pytz
from dotenv import load_dotenv
import os
from models import db, bcrypt

# Initialize extensions
mail = Mail()
login_manager = LoginManager()
serializer = None
IST = pytz.timezone('Asia/Kolkata')

def create_app():
    global serializer
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Flask Configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///garden_go.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1']
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

    # Ensure all required configurations are set
    required_configs = ['MAIL_SERVER', 'MAIL_USERNAME', 'MAIL_PASSWORD', 'SECRET_KEY']
    for config in required_configs:
        if not app.config[config]:
            raise ValueError(f"{config} is not configured in the .env file")

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'authenticate.auth'
    CORS(app)

    # Serializer for tokens
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    # Database migration setup
    migrate = Migrate(app, db)

    # Import and register blueprints
    from customer import app as customer_app
    from courier import app as courier_app
    from authenticate import app as auth_app
    from admin import app as admin_app
    from misc import app as misc_app
    from analytics import analytics_bp as analytics_app

    app.register_blueprint(customer_app)
    app.register_blueprint(courier_app)
    app.register_blueprint(admin_app)
    app.register_blueprint(auth_app)
    app.register_blueprint(misc_app)
    app.register_blueprint(analytics_app)

    # User loader for Flask-Login
    from models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Teardown session after each request
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    # Error handling
    @app.errorhandler(404)
    def page_not_found(e):
        return {"error": "Page not found"}, 404

    @app.errorhandler(500)
    def internal_error(e):
        return {"error": "Internal server error"}, 500

    return app

if __name__ == '__main__':
    app = create_app()

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Run the app
    app.run(debug=os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1'])
