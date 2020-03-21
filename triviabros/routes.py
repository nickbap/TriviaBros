from triviabros import app, db
from triviabros.forms import SignUpForm, LoginForm
from triviabros.models import User
from flask import render_template, url_for, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data,
                 password=generate_password_hash(form.password.data))

        db.session.add(u)
        db.session.commit()

        flash("Successful sign up for '{}'".format(form.username.data))
        return redirect(url_for('home'))
    return render_template('sign-up.html', form=form)


@app.route('/login-up', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login Successful!')
            return redirect(url_for('home'))
        else:
            flash('Something went wrong with your login. Please try again!')
    return render_template('login.html', form=form)


@app.route('/hidden')
@login_required
def hidden():
    return 'If you can see this, you are logged into your account!'


@app.route('/logout')
def logout():
    logout_user()
    print('User should be logged out now.')
    return redirect(url_for('home'))
