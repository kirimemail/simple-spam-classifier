import enum


class TaskStatus(enum.Enum):
    PENDING = "pending"
    COMPLETE = "complete"
    DROPPED = "dropped"


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
