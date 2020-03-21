from triviabros import app, db
from triviabros.forms import SignUp
from triviabros.models import User
from flask import render_template, url_for, flash, redirect
from werkzeug.security import generate_password_hash


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
