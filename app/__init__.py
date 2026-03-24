from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

    # Register the SMS routes
    from app.routes.sms import sms_bp
    app.register_blueprint(sms_bp)

    return app