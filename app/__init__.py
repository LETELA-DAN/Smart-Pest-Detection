# Inside app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Add this simple route to test the "Live" status
    @app.route('/')
    def index():
        return "🌱 Smart-Pest-Detection is LIVE!"

    # IMPORTANT: If you have your SMS logic in a different file (like routes.py),
    # you must register its Blueprint here:
    # from .main import bp as main_bp
    # app.register_blueprint(main_bp)

    return app