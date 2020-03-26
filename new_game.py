from triviabros import db
from triviabros.models import Question, Answer

# This script will delete all records in the `questions` and `answers` table
# so that a new game can be played. Please use with caution as it cannot be
# undone once it has run!

question_num = db.session.query(Question).delete()
answer_num = db.session.query(Answer).delete()

db.session.commit()

print("Successfully deleted {} questions!".format(question_num))
print("Successfully deleted {} answers!".format(answer_num))
