from triviabros.models import Question
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

QUESTION_NUMBER_CHOICES = [('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5),
                           ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10)]


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
    question_number = SelectField(
        'Question Number', choices=QUESTION_NUMBER_CHOICES)
    question = StringField('Question', validators=[DataRequired()])
    correct_answer = StringField('Correct Answer', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_question_number(self, question_number):
        print(question_number.data)
        question = Question.query.filter_by(author=current_user).filter_by(
            question_number=question_number.data).first()
        if question:
            raise ValidationError(
                'This Question Number has already been used. Please choose the next number.')


class AnswerForm(FlaskForm):
    answer = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('Submit')
