from app import db
from datetime import time

class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120),nullable = False,unique = True)
    password = db.Column(db.String(256),nullable = False)

class User(db.Model):
    usr_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(256),nullable = False)
    qualification = db.Column(db.String(32))
    dob = db.Column(db.Date)

class Subject(db.Model):
    sub_id = db.Column(db.Integer, primary_key=True)
    sub_name = db.Column(db.String(100), nullable=False, unique=True)
    sub_description = db.Column(db.Text, nullable=True)

    chapters = db.relationship("Chapter", backref="subject", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return self.sub_description

class Chapter(db.Model):
    chap_id = db.Column(db.Integer, primary_key=True)
    chap_name = db.Column(db.String(150), nullable=False)
    chap_description = db.Column(db.Text, nullable=True)
    sub_id = db.Column(db.Integer, db.ForeignKey('subject.sub_id'), nullable=False)

    quizzes = db.relationship("Quiz", backref="chapter", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return self.chap_description

class Quiz(db.Model):
    quiz_id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.chap_id'), nullable=False)
    quiz_name = db.Column(db.String(150),nullable = False , unique = True)
    date_of_quiz = db.Column(db.Date, nullable=False)
    time_duration = db.Column(db.Time, nullable=False)
    remarks = db.Column(db.Text, nullable=True)

    questions = db.relationship('Question', backref='quiz', cascade="all, delete, delete-orphan")
    scores = db.relationship('Score', backref='quiz', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return time.strftime(self.time_duration,"%H:%M")


class Question(db.Model):
    qtn_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=True)  
    option4 = db.Column(db.String(255), nullable=True)
    correct_option = db.Column(db.Integer, nullable=False)
    
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.usr_id'), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, nullable = False)
    total_scored = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref=db.backref('scores', lazy=True))
    

