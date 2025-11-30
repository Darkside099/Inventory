from flask import Flask, redirect, url_for
from config import Config
from extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    from routes.auth_routes import auth_bp
    from routes.inventory_routes import inventory_bp
    from routes.branch_routes import branch_bp
    from routes.report_routes import report_bp
    from routes.alert_routes import alert_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(branch_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(alert_bp)

    @app.route('/')
    def index():
        return redirect(url_for('inventory.dashboard'))

    from models.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
