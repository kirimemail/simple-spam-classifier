from .stemmer import SelectStemmedCountVectorizer, StemmedCountVectorizer
from nltk.corpus import stopwords
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, GaussianNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.feature_selection import SelectKBest, chi2, f_classif, mutual_info_classif
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, cross_validate
from sklearn.externals import joblib
import numpy as np
import os, pickle
from abc import abstractmethod
from config import Config
from app.util import LabelSwitcher


class DataDumper(object):
    def __init__(self, use="pickle"):
        self.use = use
        if not os.path.exists('spam_model'):
            os.mkdir('spam_model')

    def save(self, data, filename="spam_model/"):
        if self.use == "pickle":
            return pickle.dump(data, open(filename + "model.pickle", 'wb'))
        else:
            return joblib.dump(data, filename + "model.gz", compress=True)

    def load(self, filename='spam_model/'):
        if self.use == "pickle":
            return pickle.load(open(filename + "model.pickle", 'rb'))
        else:
            return joblib.load(filename + "model.gz")

    def clear(self, filename='spam_model/'):
        if self.use == "pickle":
            if os.path.isfile(filename + "model.pickle"):
                os.remove(filename + "model.pickle")
                return True
        else:
            if os.path.isfile(filename + "model.gz"):
                os.remove(filename + "model.gz")
                return True
        return False


class Classifier(object):
    @abstractmethod
    def train_and_test(self, train_data, test_data):
        pass

    @abstractmethod
    def classify(self, message, get_percentage=False):
        pass

    @abstractmethod
    def get_metric(self):
        pass


class SpamClassifierFacade(object):
    available_method = []

    def __init__(self, config: Config, train_data, test_data):
        self.classifier = dict()
        self.config = config
        self.train_data = train_data
        self.test_data = test_data
        self.available_method = config.ACTIVE_CLASSIFIER.split(',')
        for method in self.available_method:
            self.classifier[method] = SkLearnClassifier(method=method, config=self.config)

    def train_and_test(self):
        for method in self.available_method:
            self.classifier[method].train_and_test(self.train_data, self.test_data)
        self.test_data = None
        self.train_data = None

    def classify(self, message, method=None):
        result = dict()
        label_switcher = LabelSwitcher()
        for mt in self.available_method:
            try:
                is_spam, prob = self.classifier[mt].classify(message, get_percentage=True)
                result[mt] = {'status': label_switcher.intlabel_to_string(is_spam), 'pSpam': prob[0, 0],
                              'pHam': prob[0, 1]}
            except Exception as err:
                print("{}".format(err))

        return result

    def get_metric(self):
        result = dict()
        for method in self.available_method:
            try:
                result[method] = self.classifier[method].get_metric()
            except Exception as err:
                print("{}".format(err))
        return result


class SkLearnClassifier(Classifier):
    pipeline = None
    vect = None
    tfidf = None
    dim = None
    clf = None

    class ClassifierSwitcher(object):
        def string_to_classifier(self, argument):
            """Dispatch method"""
            method_name = 'classifier_' + str(argument)
            # Get the method from 'self'. Default to a lambda.
            method = getattr(self, method_name, self.classifier_MultinomialNB())
            # Call the method as we return it
            return method()

        def string_to_param(self, argument):
            """Dispatch method"""
            method_name = 'param_' + str(argument)
            # Get the method from 'self'. Default to a lambda.
            method = getattr(self, method_name, self.classifier_MultinomialNB())
            # Call the method as we return it
            return method()

        def classifier_MultinomialNB(self):
            return MultinomialNB(fit_prior=False)

        def param_MultinomialNB(self):
            return {'vect__ngram_range': [(1, 1), (1, 2)],
                    'vect__max_features': (None, 3000, 6000),
                    'tfidf__use_idf': (True, False),
                    'clf__alpha': (1e-2, 1e-3),
                    'clf__fit_prior': (True, False),
                    }

        def classifier_LinearSVC(self):
            return LinearSVC(loss='hinge')

        def param_LinearSVC(self):
            return {'vect__ngram_range': [(1, 1), (1, 2)],
                    'vect__max_features': (None, 3000, 6000),
                    'tfidf__use_idf': (True, False),
                    'clf__penalty': ('l1', 'l2'),
                    'clf__loss': ('hinge', 'squared_hinge'),
                    'clf__random_state': (None, 42),
                    'clf__max_iter': (1000, 2000),
                    }

        def classifier_SGDClassifier(self):
            return SGDClassifier(loss='hinge', alpha=1e-3, n_iter=5, random_state=42)

        def param_SGDClassifier(self):
            return {'vect__ngram_range': [(1, 1), (1, 2)],
                    'vect__max_features': (None, 3000, 6000),
                    'tfidf__use_idf': (True, False),
                    'clf__penalty': ('l1', 'l2'),
                    'clf__loss': ('hinge', 'squared_hinge'),
                    'clf__random_state': (None, 42),
                    'clf__max_iter': (None, 1000),
                    'clf__alpha': (1e-2, 1e-3),
                    'clf__n_iter': (None, 5),
                    }

        def classifier_BernoulliNB(self):
            return BernoulliNB(binarize=0.0, fit_prior=False)

        def param_BernoulliNB(self):
            return {'vect__ngram_range': [(1, 1), (1, 2)],
                    'vect__max_features': (None, 3000, 6000),
                    'tfidf__use_idf': (True, False),
                    'clf__alpha': (1e-2, 1e-3),
                    'clf__fit_prior': (True, False),
                    }

        def classifier_GaussianNB(self):
            return GaussianNB()

        def param_GaussianNB(self):
            return {'vect__ngram_range': [(1, 1), (1, 2)],
                    'vect__max_features': (None, 3000, 6000),
                    'tfidf__use_idf': (True, False),
                    }

    class SelectKBestSwitcher(object):
        def string_to_scorefunc(self, argument):
            """Dispatch method"""
            method_name = 'classifier_' + str(argument)
            # Get the method from 'self'. Default to a lambda.
            method = getattr(self, method_name, self.classifier_chi2())
            # Call the method as we return it
            return method()

        def classifier_f_classif(self):
            return f_classif

        def classifier_mutual_info_classif(self):
            return mutual_info_classif

        def classifier_chi2(self):
            return chi2

    def __init__(self, method, config: Config):
        classifier_switcher = self.ClassifierSwitcher()
        score_switcher = self.SelectKBestSwitcher()
        self.config = config
        self.stop_word = None
        if config.STOP_WORDS == 'all':
            self.stop_word = stopwords.words()
        else:
            self.stop_word = stopwords.words(config.STOP_WORDS)

        if config.USE_STEMMER and config.USE_MULTI_LANGUAGE_STEMMER:
            self.vect = StemmedCountVectorizer(stop_words=self.stop_word, ngram_range=(1, 2))
        elif config.USE_STEMMER:
            self.vect = SelectStemmedCountVectorizer(stop_words=self.stop_word, ngram_range=(1, 2),
                                                     stemmer_language=config.STEMMER_LANGUAGE)
        else:
            self.vect = CountVectorizer(stop_words=self.stop_word, ngram_range=(1, 2))

        self.tfidf = TfidfTransformer()
        self.dim = SelectKBest(score_switcher.string_to_scorefunc(self.config.KBEST_FUNCT), k=self.config.KBEST_COMP)
        self.clf = classifier_switcher.string_to_classifier(method)
        self.pipeline = Pipeline([
            ('vect', self.vect),
            ('tfidf', self.tfidf),
            ('dim', self.tfidf),
            ('clf', self.clf),
        ])
        self.parameters = classifier_switcher.string_to_param(method)
        self.model = None

    def classify(self, messsage, get_percentage=False):
        if get_percentage:
            return int(self.pipeline.predict([messsage])), self.pipeline.predict_log_proba([messsage])
        return int(self.pipeline.predict([messsage]))

    def train_and_test(self, train_data, test_data):
        temp_clf = self.pipeline.fit(train_data['message'], train_data['label'])
        gsf_clf = GridSearchCV(temp_clf, self.parameters, n_jobs=-1)
        self.model = gsf_clf.fit(train_data['message'], train_data['label'])
        score = cross_validate(self.model, test_data['message'], test_data['label'], n_jobs=-1,
                               scoring=['accuracy', 'f1', 'recall', 'precision'])
        self.accuracy = np.mean(score['test_accuracy'])
        self.f1 = np.mean(score['test_f1'])
        self.recall = np.mean(score['test_recall'])
        self.precision = np.mean(score['test_precision'])

    def get_metric(self):
        return {'Precision': self.precision, 'Recall': self.recall, 'F1-Score': self.f1, 'Accuracy': self.accuracy}
