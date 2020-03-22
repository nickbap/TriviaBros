from triviabros import app, db
from triviabros.forms import SignUpForm, LoginForm, QuestionForm, AnswerForm
from triviabros.models import User, Question, Answer
from flask import render_template, url_for, flash, redirect, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user


@app.route('/')
def home():
    if current_user.is_authenticated:
        users = User.query.all()
    else:
        users = None
    return render_template('home.html', users=users)


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


@app.route('/add-questions', methods=['GET', 'POST'])
@login_required
def add_questions():
    form = QuestionForm()
    questions = Question.query.filter_by(author=current_user)
    if form.validate_on_submit():
        q = Question(question_number=form.question_number.data,
                     question=form.question.data, author=current_user)

        db.session.add(q)
        db.session.commit()

        return redirect(url_for('add_questions'))
    return render_template('add-questions.html', form=form, questions=questions)


@app.route('/questions/<username>')
@login_required
def show_questions(username):
    if current_user.username == username:
        page = request.args.get('page', 1, type=int)
        questions = Question.query.filter_by(
            author=current_user).paginate(page=page, per_page=1)
        return render_template('show-questions.html', questions=questions, username=username)
    else:
        form = AnswerForm()
        # Return only questions not answered by the current user
        user = User.query.filter_by(username=username).first()
        questions_answered = Answer.get_answered_questions_for_user(
            username=current_user)
        questions = Question.query.filter_by(author=user).filter(
            ~Question.id.in_(questions_answered)).all()
        return render_template('answer-questions.html', form=form, questions=questions, username=username)


@login_required
@app.route('/submit-answers/<username>/<int:question_id>', methods=['POST'])
def submit_answers(username, question_id):
    print(request.data)
    question = Question.query.filter_by(id=question_id).first()
    a = Answer(answer=request.form['answer'],
               author=current_user, question=question)

    db.session.add(a)
    db.session.commit()
    return redirect(url_for('show_questions', username=username))


@app.route('/hidden')
@login_required
def hidden():
    return 'If you can see this, you are logged into your account!'


@app.route('/logout')
def logout():
    logout_user()
    print('User should be logged out now.')
    return redirect(url_for('home'))