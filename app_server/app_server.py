import logging

from celery import Celery
from flask import Flask
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

from app_server.config import JWT_SECRET, CELERY_BROKER_URL
from app_server.db_connection import db
from middleware.response import register_middleware


def create_app_server():

    app = Flask(__name__)
    app.config['secret_key'] = JWT_SECRET
    app.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL
    app.config['CELERY_RESULT_BACKEND'] = CELERY_BROKER_URL
    app.config['CELERY_IMPORTS'] = ("tasks.qna", )

    app.logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('flask-logging/app.log')
    app.logger.addHandler(handler)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qna_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    SWAGGER_URL = "/swagger"
    API_URL = "/static/swagger.json"
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'QnA API'
        }
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    app = register_middleware(app)

    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    return app, celery
