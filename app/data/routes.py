from app.models import TrainingData, TestData
from app.data import bp
from flask import jsonify, request
from app.data.forms import *
from app.tasks import detect_language


@bp.route('/training_data', methods=['GET'])
def get_all_training_data():
    form = GetterForm(request.args)
    result = {'limit': form.limit.data, 'page': form.page.data, 'status': 'success'}
    if form.validate():
        training_data = TrainingData.get_by(limit=form.limit.data, offset=form.get_offset())
        data = []
        for item in training_data:  # type: TrainingData
            data.append(item.serialize(exclude=['created_at', 'modified_at']))
        result['data'] = data
        result['data_count'] = len(training_data)
        result['total_page'] = TrainingData.get_page(limit=form.limit.data)
    else:
        result['error'] = form.get_error()
        result['status'] = 'error'
    return jsonify(result)


@bp.route('/training_data', methods=['POST'])
def add_training_data():
    form = DataForm()
    result = {'status': 'success'}
    if form.validate():
        data = TrainingData()
        form.populate_obj(data)
        rst, message = data.save()
        if rst:
            detect_language.delay(data.serialize())
            result['data'] = data.serialize(exclude=['created_at', 'modified_at'])
        else:
            result['status'] = 'error'
            result['error'] = message
    else:
        result['status'] = 'error'
        result['error'] = form.get_error()
    return jsonify(result)


@bp.route('/training_data/<id>', methods=['PUT', 'PATCH'])
def update_training_data(id):
    form = DataForm()
    result = {'status': 'success'}
    if form.validate():
        data = TrainingData.get_one_by({'id': id})  # type: TrainingData
        if data.__class__ is TrainingData:
            form.populate_obj(data)
            detect_language.delay(data.serialize())
            rst, message = data.save()
            if rst:
                result['data'] = data.serialize(exclude=['created_at', 'modified_at'])
            else:
                result['status'] = 'error'
                result['error'] = message
        else:
            result['status'] = 'error'
            result['error'] = "Data can't be found"
            result['id'] = id
    else:
        result['status'] = 'error'
        result['error'] = form.get_error()
    return jsonify(result)


@bp.route('/training_data/<id>', methods=['DELETE'])
def delete_training_data(id):
    result = {'status': 'success'}
    data = TrainingData.get_one_by({'id': id})  # type: TrainingData
    if data.__class__ == TrainingData:
        rst, message = data.delete()
        if not rst:
            result['status'] = 'error'
            result['message'] = message
    return jsonify(result)


@bp.route('/training_data/<id>', methods=['GET'])
def get_training_data(id):
    result = {'status': 'success'}
    data = TrainingData.get_one_by({'id': id})  # type: TrainingData
    if data is None:
        result['status'] = 'error'
        result['message'] = "Data can't be found"
    else:
        result['data'] = data.serialize(exclude=['created_at', 'modified_at'])
    return jsonify(result)


@bp.route('/test_data', methods=['GET'])
def get_all_test_data():
    form = GetterForm(request.args)
    result = {'limit': form.limit.data, 'page': form.get_offset(), 'status': 'success'}
    if form.validate():
        test_data = TestData.query.limit(form.limit.data).offset(form.get_offset()).all()
        data = []
        for item in test_data:  # type: TestData
            data.append(item.serialize(exclude=['created_at', 'modified_at']))
        result['data'] = data
        result['data_count'] = len(test_data)
        result['page_count'] = TestData.get_page(limit=form.limit.data)
    else:
        result['error'] = form.get_error()
        result['status'] = 'error'
    return jsonify(result)


@bp.route('/test_data', methods=['POST'])
def add_test_data():
    form = DataForm()
    result = {'status': 'success'}
    if form.validate():
        data = TestData()
        form.populate_obj(data)
        detect_language.delay(data.serialize())
        rst, message = data.save()
        if rst:
            result['data'] = data.serialize(exclude=['created_at', 'modified_at'])
        else:
            result['status'] = 'error'
            result['error'] = message
    else:
        result['status'] = 'error'
        result['error'] = form.get_error()
    return jsonify(result)


@bp.route('/test_data/<id>', methods=['PUT', 'PATCH'])
def update_test_data(id):
    form = DataForm()
    result = {'status': 'success'}
    if form.validate():
        data = TestData.get_one_by({'id': id})  # type: TestData
        if data.__class__ is TestData:
            form.populate_obj(data)
            detect_language.delay(data.serialize())
            rst, message = data.save()
            if rst:
                result['data'] = data.serialize(exclude=['created_at', 'modified_at'])
            else:
                result['status'] = 'error'
                result['error'] = message
        else:
            result['status'] = 'error'
            result['error'] = "Data can'data be found"
            result['id'] = id
    else:
        result['status'] = 'error'
        result['error'] = form.get_error()
    return jsonify(result)


@bp.route('/test_data/<id>', methods=['DELETE'])
def delete_test_data(id):
    result = {'status': 'success'}
    data = TestData.get_one_by({'id': id})  # type: TestData
    if data.__class__ == TestData:
        rst, message = data.delete()
        if not rst:
            result['status'] = 'error'
            result['message'] = message
    return jsonify(result)


@bp.route('/test_data/<id>', methods=['GET'])
def get_test_data(id):
    result = {'status': 'success'}
    t = TestData.get_one_by({'id': id})  # type: TestData
    if t is None:
        result['status'] = 'error'
        result['message'] = "Data can't be found"
    else:
        result['data'] = t.serialize(exclude=['created_at', 'modified_at'])
    return jsonify(result)
