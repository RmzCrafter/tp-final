from flask import Flask
from flask_cors import CORS
from app.config.config import DEBUG
from app.utils.db_utils import create_tables
from app.controllers.sentiment_controller import sentiment_bp
from app.utils.scheduler import init_scheduler

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(sentiment_bp, url_prefix='/api/sentiment')
    
    # Create database tables
    create_tables()
    
    # Initialize the scheduler
    init_scheduler()
    
    return app
