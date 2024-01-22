from flask import Flask
from flask_migrate import Migrate
from app.models.dbmodel import db
from app.routes.blueprint import user_blueprint
from config import configdb
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.configdb')

    db.init_app(app)

    return app
app = create_app()
app.register_blueprint(user_blueprint)
migrate = Migrate(app, db)
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
