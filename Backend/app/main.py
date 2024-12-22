from flask import Flask
from models import db
from routes import bp
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)

    # Configure the app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

    # Initialize database
    db.init_app(app)

    # Register routes
    app.register_blueprint(bp)

    # Ensure database is initialized
    with app.app_context():
        db.create_all()

    return app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
