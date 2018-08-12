from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from app.error import FormErrorMixin


class ClassifyForm(FlaskForm, FormErrorMixin):
    class Meta:
        csrf = False

    subject = StringField('subject', validators=[DataRequired()])
    body = TextAreaField('body', validators=[DataRequired()])
