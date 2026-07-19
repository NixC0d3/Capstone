from flask import Flask, jsonify
from .config import Config
from .extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.auth_routes import auth_bp
    from app.routes.organisation_routes import organisation_bp
    from app.routes.review_routes import review_bp
    from app.routes.recommendation_routes import recommendation_bp
    from app.routes.volunteer_routes import volunteer_bp
    from app.routes.message_routes import message_bp
    from app.routes.report_routes import report_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(organisation_bp, url_prefix="/api/organisations")
    app.register_blueprint(review_bp, url_prefix="/api/reviews")
    app.register_blueprint(recommendation_bp, url_prefix="/api/recommendations")
    app.register_blueprint(volunteer_bp, url_prefix="/api/volunteers")
    app.register_blueprint(message_bp, url_prefix="/api/messages")
    app.register_blueprint(report_bp, url_prefix="/api/reports")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    @app.route("/")
    @app.route("/api/health")
    def health_check():
        return jsonify(message="CivilInfoHub API is running")

    return app

app = create_app()

# Keep the original starter view helpers available.
from app import views
