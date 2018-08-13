from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from app.error import FormErrorMixin
from app.util import AvailableMethod


class MethodValidator(object):
    def __init__(self):
        self.message = "Method not available"

    def __call__(self, form, field):
        validation = AvailableMethod.has_value(field.data)
        if not validation:
            raise ValidationError(self.message)


class ClassifyForm(FlaskForm, FormErrorMixin):
    class Meta:
        csrf = False

    subject = StringField('subject', validators=[DataRequired()])
    body = TextAreaField('body', validators=[DataRequired()])
    method = StringField('method', default='MultinomialNB', validators=[MethodValidator()])

    def get_message(self):
        return self.subject.data + " " + self.body.data


class MethodForm(FlaskForm, FormErrorMixin):
    class Meta:
        csrf = False

    method = StringField('method', default='MultinomialNB', validators=[MethodValidator()])
