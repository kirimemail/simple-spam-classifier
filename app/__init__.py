from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import logging
from logging.handlers import RotatingFileHandler
from app.queue import FlaskCelery
from flask_basicauth import BasicAuth

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
celery = FlaskCelery()
basic_auth = BasicAuth()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['TRAIN_PERIOD_LIMIT'] = config.TRAIN_PERIOD_LIMIT
    app.config['MODEL_PERSISTENCE'] = config.MODEL_PERSISTENCE
    app.config['STOP_WORDS'] = config.STOP_WORDS
    app.config['KBEST_FUNCT'] = config.KBEST_FUNCT
    app.config['KBEST_COMP'] = config.KBEST_COMP
    app.config['USE_STEMMER'] = config.USE_STEMMER
    app.config['USE_MULTI_LANGUAGE_STEMMER'] = config.USE_MULTI_LANGUAGE_STEMMER
    app.config['STEMMER_LANGUAGE'] = config.STEMMER_LANGUAGE
    db.init_app(app)
    migrate.init_app(app, db)
    celery.init_app(app)
    basic_auth.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.data import bp as data_bp
    app.register_blueprint(data_bp)

    logger = logging.getLogger()
    logger.setLevel(app.config['LOG_LEVEL'])

    if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logger.level)
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/spam-classifier.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logger.level)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logger.level)
    app.logger.info('Simple Spam Classifier startup')

    return app


def get_celery():
    return celery


from app import models
