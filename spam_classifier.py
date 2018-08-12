from app import create_app, get_celery, cli, db
from app.models import *
from app.util import TaskStatus
from config import Config

app = create_app(Config)
cli.register(app)
celery = get_celery()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'TrainingData': TrainingData, 'TestData': TestData, 'Task': Task, 'SpamModel': SpamModel,
            'TaskStatus': TaskStatus}
