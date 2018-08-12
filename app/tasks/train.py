from app import celery, app, db
from app.models import TrainingData, TestData, prepare_data_for_training, Task, SpamModel, check_connection
from EmailProcessing import SpamClassifierFacade, DataDumper
from app.util import *
import json
from config import Config
from flask import current_app


@celery.task
def train_model(task_d):
    """
    Train spam model
    """
    task_data = json.loads(task_d, object_hook=as_enum)
    spam_data = json.loads(task_data['description'], object_hook=as_enum)
    task = Task.get_one_by({'id': task_data['id']})  # type: Task
    spam_model = SpamModel.get_one_by({'id': spam_data['id']})  # type: SpamModel
    try:
        app.logger.info("prepare data")
        train_data, test_data = prepare_data_for_training()
        app.logger.info("prepare training")
        config = Config()
        spam_classifier = SpamClassifierFacade(config, train_data=train_data, test_data=test_data)
        app.logger.info("start training")
        spam_classifier.train_and_test()
        app.logger.info("dumping model")
        dumper = DataDumper(config.MODEL_PERSISTENCE)
        dumper.save(spam_classifier)
        app.logger.info("check connection")
        check_connection()
        app.logger.info("save model")
        spam_model.status = TaskStatus.COMPLETE
        spam_model.save()
        task.status = TaskStatus.COMPLETE
        task.description = json.dumps(spam_model.serialize(exclude=['created_at', 'modified_at']), cls=JsonEncoder)
        task.save()
        return True
    except Exception as err:
        app.logger.error("Error : {}".format(err))
        check_connection()
        spam_model.status = TaskStatus.DROPPED
        spam_model.save()
        task.status = TaskStatus.DROPPED
        task.description = json.dumps(spam_model.serialize(exclude=['created_at', 'modified_at']), cls=JsonEncoder)
        task.save()
        return False
