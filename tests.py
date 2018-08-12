#!/usr/bin/env python

import unittest
from app import create_app, db
from app.models import TrainingData, TestData
from config import Config
import sys

if sys.version_info >= (3, 5):
    from importlib.util import spec_from_file_location


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


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
        db.session.add(traindata)
        db.session.add(testdata)
        db.session.commit()
        self.assertEqual(traindata.id, 1)
        self.assertEqual(testdata.id, 1)
        self.assertEqual(traindata.subject, 'train')
        self.assertEqual(testdata.subject, 'test')


if __name__ == '__main__':
    unittest.main(verbosity=2)
