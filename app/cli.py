from app.tasks import multiply, train_model
import os, click, json
from flask.cli import with_appcontext
from app.models import *
from flask import current_app
from app.helper import start_train
from EmailProcessing import LanguageDetection


def register(app):
    @app.cli.group()
    def database():
        """
        Perform addition database commands
        """
        pass

    def get_data_seed(directory):
        """
        Get Seed Data
        :param directory:
        :return:
        """
        result = list()
        for i in os.listdir('seeds/' + directory):
            for j in os.listdir('seeds/' + directory + '/' + str(i)):
                label = 0
                if i == 'ham':
                    label = 1
                try:
                    subject = ""
                    body = ""
                    with open('seeds/' + directory + '/' + str(i) + '/' + str(j)) as m:

                        for k, line in enumerate(m):
                            try:
                                if k == 0:
                                    subject = line.replace('Subject:', '').strip()
                                else:
                                    body = body + " " + line.strip()
                            except Exception as err:
                                print("Line error: {}".format(err))
                    # print('Subject: {}\nBody:{}'.format(subject, body))
                    result.append({'subject': subject, 'body': body, 'label': label})
                except Exception as err:
                    print("Open error:{}".format(err))
        return result

    @database.command()
    def seed():
        """
        Run seeding
        """
        if has_been_seed() is False:
            print("Run seeding train")
            train_data = get_data_seed('train_mails')
            lang_detect = LanguageDetection()
            for item in train_data:
                train_d = TrainingData(subject=item['subject'], body=item['body'], label=item['label'])
                train_d.lang = lang_detect.detect_language(train_d.get_message())
                train_d.save()
            test_data = get_data_seed('test_mails')
            for item in test_data:
                test_d = TestData(subject=item['subject'], body=item['body'], label=item['label'])
                test_d.lang = lang_detect.detect_language(train_d.get_message())
                test_d.save()
        pass

    @app.cli.group()
    def example():
        """
        Example cli task
        """
        pass

    @example.command()
    def multiple():
        result = multiply.delay(10, 10)
        print(result.wait())
        pass

    @app.cli.command()
    def train():
        """
        Run train task
        """
        result = start_train()
        print(json.dumps(result))
