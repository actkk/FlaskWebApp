from flask import Flask
from flask_migrate import Migrate
from app.models.dbmodel import db
from app.routes.blueprint import user_blueprint
from app.log.logger import setup_logging




def create_app():
    app = Flask(__name__)
    app.config.from_object('config.configdb')

    # Initialize database with the Flask app
    db.init_app(app)

    # Register the blueprint within the create_app function
    app.register_blueprint(user_blueprint)

    # Initialize Flask-Migrate with the app and database
    migrate = Migrate(app, db)

    # Create the database if it does not exist
    with app.app_context():
        db.create_all()
    setup_logging(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
