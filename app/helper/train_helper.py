from datetime import datetime
import tzlocal, time, json
from app.models import SpamModel, Task
from app.util import TaskStatus, JsonEncoder, AvailableMethod
from flask import current_app
from app.tasks import train_model


def start_train(method="MultinomialNB"):
    """
    Helper to start training process, for cli or api
    :return:
    """
    result = {'status': 'error', 'code': 2, 'hours_limit': current_app.config['TRAIN_PERIOD_LIMIT']}
    if AvailableMethod.has_value(method):
        spam_model = SpamModel.get_last_record({"classifier": method})  # type: SpamModel
        if spam_model is None or (spam_model is not None and (
                spam_model.status == TaskStatus.COMPLETE or spam_model.status == TaskStatus.DROPPED or time.time() - spam_model.created_at >
                result[
                    'hours_limit'])):
            result['code'] = 1
            spam_model = SpamModel(status="PENDING", classifier=method)
            spam_model.save()
            task = Task(name='train',
                        description=json.dumps(spam_model.serialize(exclude=['created_at', 'modified_at']),
                                               cls=JsonEncoder),
                        status="PENDING")
            task.save()
            train_model.delay(json.dumps(task.serialize(), cls=JsonEncoder), method)
            result['code'] = 0
            result['status'] = 'success'
            result['message'] = 'Training ' + method + ' started'
        else:
            if spam_model is not None:
                local_timezone = tzlocal.get_localzone()  # get pytz timezone
                local_time = datetime.fromtimestamp(spam_model.created_at, local_timezone)
                result['message'] = 'Training can\'t be started yet. Last started : {}'.format(
                    local_time.strftime("%Y-%m-%d %H:%M:%S (%Z %z)"))
    else:
        result['message'] = "Method not available"
    return result
