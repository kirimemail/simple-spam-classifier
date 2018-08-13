import enum


class TaskStatus(enum.Enum):
    PENDING = "pending"
    COMPLETE = "complete"
    DROPPED = "dropped"


class AvailableMethod(enum.Enum):
    MultinomialNB = "MultinomialNB"
    BernoulliNB = "BernoulliNB"
    GaussianNB = "GaussianNB"
    LinearSVC = "LinearSVC"
    SGDClassifier = "SGDClassifier"
    AdaBoostClassifier = "AdaBoostClassifier"
    MLPClassifier = "MLPClassifier"

    @classmethod
    def has_value(cls, value):
        return (value == item.value for item in cls)


class LabelSwitcher(object):
    def intlabel_to_string(self, argument):
        """Dispatch method"""
        method_name = 'label_' + str(argument)
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, "None")
        # Call the method as we return it
        return method()

    def label_0(self):
        return "SPAM"

    def label_1(self):
        return "HAM"
