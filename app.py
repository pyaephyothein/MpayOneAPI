# app.py
import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from config import DATABASE_URL

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

# Create the SQLAlchemy db instance
db = SQLAlchemy(model_class=Base)

def create_app():
    app = Flask(__name__)
    
    # Setup a secret key
    app.secret_key = os.environ.get("SESSION_SECRET", "mpay_one_secret_key")
    
    # Configure the database
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the app with SQLAlchemy
    db.init_app(app)

    return app
