from triviabros.models import Question, User
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

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "It looks this username already exists. \
                     Please choose a different name!")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError(
                "It looks like you've already signed up with this email. \
                     Please use a different email address!")


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
