from triviabros import db, login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    questions = db.relationship('Question', backref='author', lazy=True)
    answers = db.relationship('Answer', backref='author', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    question_number = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    answers = db.relationship('Answer', backref='question', lazy=True)

    def __repr__(self):
        return '<Question {} {}>'.format(self.question, self.user_id)


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    answer = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'questions.id'), nullable=False)

    @staticmethod
    def get_answered_questions_for_user(username):
        """Returns question ids for questions answered for given username object"""
        answers = Answer.query.filter_by(author=username).all()
        question_ids = []
        for answer in answers:
            question_ids.append(answer.question_id)
        return question_ids

    def __repr__(self):
        return '<Answer {} {} {}>'.format(self.answer, self.user_id, self.question_id)
