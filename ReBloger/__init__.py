from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from config import config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'manager.login'
admin = Admin()


class ReBlogerException(Exception):
    code = 0

    def to_json(self):
        return dict(code=self.code, msg=self.msg)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)

    from general import general as general_blueprint
    from manager import manager as manager_blueprint
    app.register_blueprint(general_blueprint)
    app.register_blueprint(manager_blueprint, url_prefix='/manager')

    return app