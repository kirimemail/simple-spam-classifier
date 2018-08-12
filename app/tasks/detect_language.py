from app import celery, app
from EmailProcessing import LanguageDetection
from app.models import TrainingData, TestData


@celery.task
def detect_language(model):
    try:
        lang = LanguageDetection()
        data = None
        if model['class'] == 'TrainingData':
            data = TrainingData.get_one_by({'id': model['id']})  # type: TrainingData
            data.lang = lang.detect_language(data.get_message())
            data.save()
        else:
            data = TestData.get_one_by({'id': model['id']})  # type: TestData
            data.lang = lang.detect_language(data.get_message())
            data.save()
        app.logger.info("Language detected : {}".format(data.lang))
        return True
    except Exception as e:
        app.logger.error("{}".format(e))
        return False
