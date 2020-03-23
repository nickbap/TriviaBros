from triviabros import db
from triviabros.models import Question, Answer


db.session.query(Question).delete()
db.session.query(Answer).delete()

db.session.commit()
