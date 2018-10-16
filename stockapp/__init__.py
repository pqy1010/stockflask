from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask import Flask,render_template

boostrap=Bootstrap()
db=SQLAlchemy()
login_manager=LoginManager()
from stockapp import view
login_manager.session_protection='strong'
login_manager.login_view='view.index'

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    boostrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(view.view)
    return app
# def create_app(test_config=None):
#     # create and configure the app
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY='dev',
#         DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
#     )
#
#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         # load the test config if passed in
#         app.config.from_mapping(test_config)
#
#     # ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass
#
#     # a simple page that says hello
#     @app.route('/hello')
#     def hello():
#         return 'Hello, World!'
#
#     from . import db
#     db.init_app(app)
#
#     return app
