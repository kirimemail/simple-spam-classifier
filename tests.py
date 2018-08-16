#!/usr/bin/env python

import unittest
from app import create_app, db
from app.models import *
from app.helper import start_train
from config import Config
import sys

if sys.version_info >= (3, 5):
    from importlib.util import spec_from_file_location


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_POOL_SIZE = None
    SQLALCHEMY_MAX_OVERFLOW = None


class TrainingDataModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add(self):
        traindata = TrainingData(subject="train", body="train", label=False)
        testdata = TestData(subject="test", body="test", label=False)
        traindata.save()
        testdata.save()
        self.assertEqual(traindata.id, 1)
        self.assertEqual(testdata.id, 1)
        self.assertEqual(traindata.subject, 'train')
        self.assertEqual(testdata.subject, 'test')

    def test_train(self):
        result = start_train("MultinomialNB")
        spam_model = SpamModel.get_first_record({'classifier': 'MultinomialNB'})  # type: SpamModel
        spam_model2 = SpamModel.get_first_record({'classifier': 'LinearSVC'})  # type: SpamModel
        self.assertEqual(result['status'], 'success')
        self.assertIsNotNone(spam_model.classifier)
        self.assertIsNone(spam_model2)

        result = start_train("MultinomialNB")
        self.assertEqual(result['status'], 'error')
        spam_model3 = SpamModel.get_first_record({'classifier': 'MultinomialNB'})  # type: SpamModel
        self.assertEqual(spam_model.serialize(), spam_model3.serialize())


if __name__ == '__main__':
    unittest.main(verbosity=2)
