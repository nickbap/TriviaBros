from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=30)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm Password', validators=[
                                          DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class QuestionForm(FlaskForm):
    question_number = IntegerField(
        'Question Number', validators=[DataRequired()])
    question = StringField('Question', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_question_number(self, question_number):
        if not isinstance(question_number.data, int):
            raise ValidationError('Must submit an Integer.')


class AnswerForm(FlaskForm):
    answer = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('Submit')
