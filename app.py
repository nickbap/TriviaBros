from flask import Flask, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-keys-are-big-secrets-for-now'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trivia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class SignUp(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=30)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm Password', validators=[
                                          DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUp()
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data,
                 password=generate_password_hash(form.password.data))

        db.session.add(u)
        db.session.commit()

        flash("Successful sign up for '{}'".format(form.username.data))
        return redirect(url_for('home'))
    return render_template('sign-up.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
