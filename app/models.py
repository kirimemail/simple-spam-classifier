from app import db, app
from flask_sqlalchemy import BaseQuery, inspect
from sqlalchemy.exc import SQLAlchemyError
import time, math
import pandas as pd
from app.util import TaskStatus


class SerializableMixin(object):

    def serialize(self, include={}, exclude=[], only=[]):
        serialized = {}
        for key in inspect(self).attrs.keys():
            to_be_serialized = True
            value = getattr(self, key)
            if key in exclude or (only and key not in only):
                to_be_serialized = False
            elif isinstance(value, BaseQuery):
                to_be_serialized = False
                if key in include:
                    to_be_serialized = True
                    nested_params = include.get(key, {})
                    value = [i.serialize(**nested_params) for i in value]

            if to_be_serialized:
                serialized[key] = value

        return serialized


class CrudableMixin(object):
    def create(self):
        try:
            self.__set_created()
            db.session.add(self)
            db.session.commit()
            return True, ""
        except SQLAlchemyError as err:
            db.session.rollback()
            app.logger.error("Error : {}".format(err))
            return False, "Error : {}".format(err)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True, ""
        except SQLAlchemyError as err:
            db.session.rollback()
            app.logger.error("Error : {}".format(err))
            return False, "Error : {}".format(err)

    def update(self):
        try:
            self.__set_updated()
            db.session.commit()
            return True, ""
        except SQLAlchemyError as err:
            db.session.rollback()
            app.logger.error("Error : {}".format(err))
            return False, "Error : {}".format(err)

    def __set_created(self):
        try:
            self.__setattr__('created_at', time.time())
            self.__setattr__('modified_at', time.time())
        except AttributeError:
            pass

    def __set_updated(self):
        try:
            self.__setattr__('modified_at', time.time())
        except AttributeError:
            pass

    def save(self):
        if not self.__data_exist():
            return self.create()
        else:
            return self.update()

    def __data_exist(self):
        primary = self.__have_primary()
        if primary is not None and len(primary) > 0:
            return True
        return False

    def __have_primary(self):
        return inspect(self).identity

    def check_connection(self):
        try:
            db.session.query(self).count()
        except Exception as err:
            app.logger.error("{}".format(err))
            db.session.rollback()


class HelperMixin(object):
    @classmethod
    def get_one_by(cls, params={}):
        return db.session.query(cls).filter_by(**params).one_or_none()

    @classmethod
    def get_by(cls, params={}, limit=100, offset=1):
        query = db.session.query(cls).filter_by(**params)
        query = query.limit(limit)
        query = query.offset(offset)
        return query.all()

    @classmethod
    def get_page(cls, limit=100):
        return int(math.floor(cls.count_all() / limit + 1))

    @classmethod
    def count_all(cls):
        return db.session.query(cls).count()

    @classmethod
    def get_first_record(cls):
        return db.session.query(cls).order_by('id').first()

    @classmethod
    def get_last_record(cls):
        return db.session.query(cls).order_by('-id').first()


class DataModel(object):
    def get_message(self):
        return self.__getattribute__('subject') + ' ' + self.__getattribute__('body')


class TrainingData(db.Model, CrudableMixin, SerializableMixin, HelperMixin, DataModel):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    label = db.Column(db.Integer, nullable=False)
    lang = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.Integer, default=0)
    modified_at = db.Column(db.Integer, default=0)

    def prepare_data(self):
        pass

    def serialize_for_data(self):
        return {'message': self.get_message(), 'label': self.label}

    def serialize(self, include={}, exclude=[], only=[]):
        result = super(TrainingData, self).serialize(include, exclude, only)
        result['class'] = 'TrainingData'
        return result

    def __repr__(self):
        return '<TrainingData {},{},{}>'.format(self.id, self.subject, ("HAM" if self.label >= 1 else "SPAM"))

    def __str__(self):
        return '<TrainingData {},{},{}>'.format(self.id, self.subject, ("HAM" if self.label >= 1 else "SPAM"))


class TestData(db.Model, CrudableMixin, SerializableMixin, HelperMixin, DataModel):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    label = db.Column(db.Integer, nullable=False)
    lang = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.Integer, default=0)
    modified_at = db.Column(db.Integer, default=0)

    def prepare_data(self):
        pass

    def serialize_for_data(self):
        return {'message': self.get_message(), 'label': self.label}

    def __repr__(self):
        return '<TestData {},{},{}>'.format(self.id, self.subject, ("HAM" if self.label >= 1 else "SPAM"))

    def __str__(self):
        return '<TestData {},{},{}>'.format(self.id, self.subject, ("HAM" if self.label >= 1 else "SPAM"))


class Task(db.Model, CrudableMixin, SerializableMixin, HelperMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    status = db.Column(db.Enum(TaskStatus))
    created_at = db.Column(db.Integer, default=0)
    modified_at = db.Column(db.Integer, default=0)


class SpamModel(db.Model, CrudableMixin, SerializableMixin, HelperMixin):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(TaskStatus))
    created_at = db.Column(db.Integer, default=0)
    modified_at = db.Column(db.Integer, default=0)


def check_connection():
    try:
        app.logger.info("{}".format(Task.count_all()))
    except Exception as err:
        app.logger.error("{}".format(err))
        db.session.rollback()


def has_been_seed():
    return TrainingData.query.count() > 0 and TestData.query.count() > 0 and SpamModel.query.count() > 0


def get_offset(page, limit=100):
    if page <= 0:
        return 1
    return (page - 1) * limit + 1


def prepare_data_for_training():
    training_data_page_count = TrainingData.get_page()
    training_data = list()
    for i in range(training_data_page_count):
        trains = TrainingData.get_by(offset=get_offset(i + 1))
        for item in trains:  # type: TrainingData
            training_data.append(item.serialize_for_data())
    test_data_page_count = TestData.get_page()
    test_data = list()
    for i in range(test_data_page_count):
        tests = TestData.get_by(offset=get_offset(i + 1))
        for item in tests:  # type: TestData
            test_data.append(item.serialize_for_data())
    return pd.DataFrame(training_data), pd.DataFrame(test_data)
