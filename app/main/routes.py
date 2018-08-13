from app.main import bp
from EmailProcessing import DataDumper, SpamClassifierFacade
from flask import jsonify, current_app
from app.main.forms import ClassifyForm, MethodForm
from app.helper import start_train
from config import Config
import os


@bp.route('/')
def hello_world():
    return jsonify({
        'app': 'SimpleSpamClassifier',
        'version': "0.1.0 alpha",
    })


@bp.route('/metric', methods=['POST'])
def info():
    form = MethodForm()
    result = {'status': 'error', 'code': 2}
    if form.validate():
        scf = SpamClassifierFacade(Config(), None, None, form.method.data)
        result['metric'] = {form.method.data: scf.get_metric()}
        result['status'] = 'success'
        result['code'] = 0
    else:
        result['message'] = form.get_error()
    return jsonify(result)


@bp.route('/train', methods=['GET'])
def train():
    form = MethodForm()
    result = {'status': 'error', 'code': 2}
    if form.validate():
        result = start_train(form.method.data)
    else:
        result['message'] = form.get_error()
    return jsonify(result)


@bp.route('/clear_model', methods=['POST'])
def clear_model():
    form = MethodForm()
    result = {'status': 'error', 'code': 2}
    if form.validate():
        scf = SpamClassifierFacade(Config(), None, None, form.method.data)
        if scf.clear():
            result['code'] = 0
            result['status'] = 'success'
            result['message'] = "{} Model is deleted. Try to start new training before classifying.".format(
                form.method.data)
        else:
            result['code'] = 1
            result['message'] = "{} Model is not exist.".format(form.method.data)
    else:
        result['message'] = form.get_error()
    return jsonify(result)


@bp.route('/classify', methods=['POST'])
def classify():
    form = ClassifyForm()
    result = {'status': 'error', 'code': 2}
    if form.validate():
        scf = SpamClassifierFacade(Config(), None, None, form.method.data)
        result = {'status': 'success', 'code': 0}
        result[form.method.data] = scf.classify(form.get_message())
    else:
        result['message'] = form.get_error()
    return jsonify(result)
