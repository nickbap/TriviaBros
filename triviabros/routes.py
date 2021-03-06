from triviabros import app, db
from triviabros.forms import SignUpForm, LoginForm, QuestionForm, AnswerForm
from triviabros.models import User, Question, Answer
from flask import render_template, url_for, flash, redirect, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user
from sqlalchemy import func, case, asc, desc


@app.route('/')
def home():
    if current_user.is_authenticated:
        users = (User.query.filter(
                 User.id.in_(db.session.query(Question.user_id)
                             .distinct())).all())
    else:
        users = None
    return render_template('home.html', users=users)


@app.route('/rules')
def rules():
    return render_template('rules.html')


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data.lower(),
                 password=generate_password_hash(form.password.data))
        db.session.add(u)
        db.session.commit()
        flash("Successful sign up for '{}'! Please login to play!".format(
            form.username.data))
        return redirect(url_for('login'))
    return render_template('sign-up.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
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
    questions = (Question.query.filter_by(author=current_user)
                 .order_by(asc('question_number')))
    if form.validate_on_submit():
        q = Question(question_number=form.question_number.data,
                     question=form.question.data, correct_answer=form.correct_answer.data, author=current_user)
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('add_questions'))
    return render_template('add-questions.html', form=form, questions=questions)


@app.route('/questions/<username>')
@login_required
def show_questions(username):
    if current_user.username == username:
        page = request.args.get('page', 1, type=int)
        questions = (Question.query.filter_by(author=current_user)
                     .order_by(asc('question_number'))
                     .paginate(page=page, per_page=1))
        return render_template('show-questions.html', questions=questions, username=username)
    else:
        form = AnswerForm()
        user = User.query.filter_by(username=username).first()
        questions_answered = Answer.get_answered_questions_for_user(
            username=current_user)
        questions = (Question.query.filter_by(author=user)
                     .order_by(asc('question_number'))
                     .filter(~Question.id.in_(questions_answered))
                     .all())
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


@login_required
@app.route('/review-answers/<username>')
def review_answers(username):
    form = AnswerForm()
    answers = (db.session.query(User, Question, Answer)
               .join(Question, Question.user_id == User.id)
               .join(Answer, Answer.question_id == Question.id)
               .filter(User.username == username)
               .filter(Answer.user_id == current_user.id)
               .order_by(asc(Question.question_number))
               .all())
    return render_template('review-answers.html', form=form, username=username, answers=answers)


@login_required
@app.route('/update-answer/<username>/<int:answer_id>', methods=['POST'])
def update_answer(username, answer_id):
    a = Answer.query.filter_by(id=answer_id).first()
    a.answer = request.form['answer']
    db.session.add(a)
    db.session.commit()
    return redirect(url_for('review_answers', username=username))


@login_required
@app.route('/grade-answers/<username>')
def grade_answers(username):
    if current_user.username == username:
        answers = (db.session.query(Answer, Question)
                   .join(Question)
                   .filter(Question.author == current_user)
                   .filter(Answer.is_correct == None)
                   .order_by(Question.question_number))
    else:
        answers = None
    return render_template('grade-answers.html', answers=answers, username=current_user.username)


def convert_to_boolean(is_correct):
    if is_correct == '1':
        return True
    else:
        return False


@login_required
@app.route('/grade-answers/<username>/<int:answer_id>')
def submit_graded_answers(username, answer_id):
    a = Answer.query.filter_by(id=answer_id).first()
    a.is_correct = convert_to_boolean(request.args.get('is_correct'))
    db.session.add(a)
    db.session.commit()
    return redirect(url_for('grade_answers', username=username))


@login_required
@app.route('/score')
def score():
    scores = (db.session.query(User.username,
                               func.sum(
                                   case([(Answer.is_correct == True, 1)], else_=0))
                               .label('points'))
              .join(Answer)
              .group_by(User.username)
              .order_by(desc('points'))
              .all())

    players = []
    player_scores = []
    for score in scores:
        players.append(score.username)
        if not score.points:
            player_scores.append(0)
        else:
            player_scores.append(int(score.points))

    data = {'players': players,
            'player_scores': player_scores}
    return render_template('score.html', scores=scores, **data)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
