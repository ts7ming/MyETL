from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    print(config_class.SQLALCHEMY_DATABASE_URI)
    db.init_app(app)
    migrate.init_app(app, db)

    from etl.ui.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
