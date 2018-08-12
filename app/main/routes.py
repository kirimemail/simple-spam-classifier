from app.main import bp
from EmailProcessing import DataDumper, SpamClassifierFacade
from flask import jsonify, current_app
from app.main.forms import ClassifyForm
from app.helper import start_train
import os


@bp.route('/')
def hello_world():
    return jsonify({
        'app': 'SimpleSpamClassifier',
        'version': "0.1.0 alpha",
    })


@bp.route('/metric', methods=['GET'])
def info():
    result = {'status': 'error', 'code': 2}
    dt = DataDumper(current_app.config['MODEL_PERSISTENCE'])
    try:
        result['code'] = 1
        classifier = dt.load()  # type: SpamClassifierFacade
        if classifier.__class__ == SpamClassifierFacade:
            rst = classifier.get_metric()
            result['status'] = 'success'
            result['code'] = 0
            result['result'] = rst
    except FileNotFoundError:
        result['code'] = 2
        result['message'] = 'Model doesn\'t exist.'
    return jsonify(result)


@bp.route('/train', methods=['GET'])
def train():
    result = start_train()
    return jsonify(result)


@bp.route('/clear_model', methods=['GET'])
def clear_model():
    dt = DataDumper(current_app.config['MODEL_PERSISTENCE'])
    result = {'status': 'No existing model', 'code': 2}
    if dt.clear():
        result = {'status': 'Model deleted. Start new train to build new model.', 'code': 0}
    return jsonify(result)


@bp.route('/classify', methods=['POST'])
def classify():
    form = ClassifyForm()
    result = {'status': 'error', 'code': 2}
    if form.validate():
        result['code'] = 1
        dt = DataDumper(current_app.config['MODEL_PERSISTENCE'])
        try:
            classifier = dt.load()  # type: SpamClassifierFacade
            if classifier.__class__ == SpamClassifierFacade:
                message = form.subject.data + " " + form.body.data
                rst = classifier.classify(message=message)
                result['result'] = {'score': rst, 'message': message}
                result['code'] = 0
                result['status'] = 'success'
        except FileNotFoundError:
            result['code'] = 2
            result['message'] = 'Model doesn\'t exist.'
    else:
        result['message'] = form.get_error()
    return jsonify(result)
