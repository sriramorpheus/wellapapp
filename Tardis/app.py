from flask import Flask
from extensions import db, migrate
from home import home_bp
from reading_mode import reading_mode_bp
from flashcards import flashcards_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tardis.db'
    app.config['SECRET_KEY'] = 'your-secret-key'

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(reading_mode_bp, url_prefix='/reading-mode')
    app.register_blueprint(flashcards_bp, url_prefix='/flashcards')

    # Log routes at startup
    with app.app_context():
        for rule in app.url_map.iter_rules():
            print(f"Endpoint: {rule.endpoint}, URL: {rule.rule}")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)