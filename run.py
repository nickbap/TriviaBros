from triviabros import app, db
from triviabros.models import User, Question, Answer


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Question': Question, 'Answer': Answer}


if __name__ == "__main__":
    app.run(debug=True)
