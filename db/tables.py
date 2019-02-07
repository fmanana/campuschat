from app import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class auth(db.Model):
    email = db.Column(db.String(255), primary_key=True, nullable=False)
    password = db.Column(db.String(1023), nullable=False)

    def __repr__(self):
        return '[email={}, pw={}]\n'.format(self.email, self.password)

class professors(db.Model):
    prof_id = db.Column(db.String(63), unique=True, nullable=False, primary_key=True)
    email = db.Column(db.String(63), db.ForeignKey('auth.email'), nullable=False)
    first_name = db.Column(db.String(63), nullable=False)
    last_name = db.Column(db.String(63), nullable=False)

    def __repr__(self):
        return 'prof_id={}\nemail={}\nfirst_name={}\nlast_name={}\n' \
            .format(self.prof_id, self.email, self.first_name, self.last_name)

class students(db.Model):
    matr_num = db.Column(db.String(63), nullable=False, primary_key=True)
    first_name = db.Column(db.String(63), nullable=False)
    last_name = db.Column(db.String(63), nullable=False)
    class_of = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(63), db.ForeignKey('auth.email'), nullable=False)
    major = db.Column(db.String(63), nullable=False)

    def __repr__(self):
        return 'matr_num={}, name={} {}, class_of={}, email={}, major={}\n' \
            .format(self.matr_num, self.first_name, self.last_name, self.class_of, \
                self.email, self.major)

class courses(db.Model):
    course_id = db.Column(db.String(63), db.ForeignKey('registrations.course_id'),\
        nullable=False, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    prof_id = db.Column(db.String(63), db.ForeignKey('professors.prof_id'),\
        nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'course_id={}, name={}, prof_id={}, year={}\n'\
            .format(self.course_id, self.name, self.prof_id, self.year)

class registrations(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    course_id = db.Column(db.String(63), db.ForeignKey('courses.course_id'),\
        nullable=False)
    matr_num = db.Column(db.String(63), db.ForeignKey('students.matr_num'),\
        nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'course_id={}, matr_num={}, year={}\n'\
            .format(self.course_id, self.matr_num, self.year)

class chats(db.Model):
    chat_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    course_id = db.Column(db.String(63), db.ForeignKey('courses.course_id'),\
        nullable=False, unique=True)
    
    def __repr__(self):
        return 'chat_id={}, course_id={}\n'.format(self.chat_id, self.course_id)

class messages(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.chat_id'),\
        nullable=False)
    sender = db.Column(db.String(63), db.ForeignKey('students.matr_num'),\
        db.ForeignKey('professors.prof_id'), nullable=False)
    sent_time = db.Column(db.DateTime, default=datetime.utcnow)
    sent_date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text)

    def __repr__(self):
        return 'id={}, chat_id={}, sender={}, sent_time={}, sent_date={} content={}'\
            .format(self.id, self.chat_id, self.sender, self.sent_time, self.sent_date, self.content)