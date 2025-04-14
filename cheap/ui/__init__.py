from flask import Flask


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from cheap.ui.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
