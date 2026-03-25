from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes.sms import sms_bp
    app.register_blueprint(sms_bp)

    return app