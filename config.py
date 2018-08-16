import os
from dotenv import load_dotenv
import string, random

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Config(object):
    FLASK_DEBUG = bool(int(os.environ.get('FLASK_DEBUG', 0))) or False
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'production'
    SECRET_KEY = os.environ.get('SECRET_KEY') or id_generator(10)
    FLASK_RUN_PORT = os.environ.get('PORT') or 8000
    FLASK_RUN_HOST = os.environ.get('HOST') or '0.0.0.0'

    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir,
                                                                                                       'app.db')
    SQLALCHEMY_RECORD_QUERIES = bool(int(os.environ.get('SQLALCHEMY_RECORD_QUERIES', 0))) or False
    SQLALCHEMY_POOL_RECYCLE = int(os.environ.get('SQLALCHEMY_POOL_RECYCLE', 299)) or 299
    SQLALCHEMY_POOL_SIZE = int(os.environ.get('SQLALCHEMY_POOL_SIZE', 20)) or 20
    SQLALCHEMY_MAX_OVERFLOW = int(os.environ.get('SQLALCHEMY_MAX_OVERFLOW', 10)) or 10

    LOG_TO_STDOUT = bool(int(os.environ.get('LOG_TO_STDOUT', 1))) or True
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'ERROR'

    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'

    TRAIN_PERIOD_LIMIT = int(os.environ.get('TRAIN_PERIOD_LIMIT', 86400)) or 86400
    BASIC_AUTH_USERNAME = os.environ.get('BASIC_AUTH_USERNAME') or 'spamclassifier'
    BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD') or '123456'
    BASIC_AUTH_FORCE = bool(int(os.environ.get('BASIC_AUTH_FORCE', 0))) or False

    KBEST_COMP = int(os.environ.get('KBEST_COMP', 2)) or 2
    KBEST_FUNCT = os.environ.get('KBEST_FUNCT') or 'chi2'
    STOP_WORDS = os.environ.get('STOP_WORDS') or 'english'
    USE_STEMMER = bool(int(os.environ.get('USE_STEMMER', 0))) or False
    USE_MULTI_LANGUAGE_STEMMER = bool(int(os.environ.get('USE_MULTI_LANGUAGE_STEMMER', 0))) or False
    STEMMER_LANGUAGE = os.environ.get('STEMMER_LANGUAGE')
    OPTIMIZE_MODEL = bool(int(os.environ.get('OPTIMIZE_MODEL', 0))) or False

    MODEL_PERSISTENCE = os.environ.get('MODEL_PERSISTENCE') or 'joblib'