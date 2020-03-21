from flask import Flask, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-keys-are-big-secrets-for-now'


class SignUp(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUp()
    if form.validate_on_submit():
        print(form.username.data)
        print(form.email.data)
        print(form.password.data)

        flash("Successful sign up for '{}'".format(form.username.data))
        return redirect(url_for('home'))
    return render_template('sign-up.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
