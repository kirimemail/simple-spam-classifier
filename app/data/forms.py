from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from app.error import FormErrorMixin


class DataForm(FlaskForm, FormErrorMixin):
    class Meta:
        csrf = False

    subject = StringField('subject', validators=[DataRequired()])
    body = TextAreaField('body', validators=[DataRequired()])
    label = BooleanField('label', validators=[DataRequired()])


class GetterForm(FlaskForm, FormErrorMixin):
    class Meta:
        csrf = False

    page = IntegerField('page', default=1, validators=[NumberRange(min=1)])
    limit = IntegerField('limit', default=100, validators=[NumberRange(min=0)])

    def get_offset(self):
        if self.page.data <= 0:
            return 1
        return (self.page.data - 1) * self.limit.data + 1
