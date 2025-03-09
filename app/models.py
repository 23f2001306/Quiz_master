import datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

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

    def __repr__(self):
        return self.sub_description

class Chapter(db.Model):
    chapter_id = db.Column(db.Integer, primary_key=True)
    chapter_name = db.Column(db.String(150), nullable=False)
    chapter_description = db.Column(db.Text, nullable=True)
    sub_id = db.Column(db.Integer, db.ForeignKey('subject.sub_id'), nullable=False)

    subject = db.relationship('Subject', backref=db.backref('chapters', lazy=True))

class Quiz(db.Model):
    quiz_id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.chapter_id'), nullable=False)
    date_of_quiz = db.Column(db.Date, nullable=False)
    time_duration = db.Column(db.Time, nullable=False)
    remarks = db.Column(db.Text, nullable=True)

    chapter = db.relationship('Chapter', backref=db.backref('quizzes', lazy=True))

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.usr_id'), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, nullable = False)
    total_scored = db.Column(db.Integer, nullable=False)

    quiz = db.relationship('Quiz', backref=db.backref('scores', lazy=True))
    user = db.relationship('User', backref=db.backref('scores', lazy=True))

