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



def get_student_by_id(id):
    res = None
    q_res = students.query.filter(students.matr_num.in_([id])).first()
    if q_res:
        res = {
            'matr_num': q_res.matr_num,
            'first_name': q_res.first_name,
            'last_name': q_res.last_name,
            'class_of': q_res.class_of,
            'major': q_res.major,
            'email': q_res.email
        }
    return res

def get_registrations(course_id=None, matr_num=None):
    res = []
    if course_id != None:
        qres = registrations.query.filter(registrations.course_id.in_([course_id])).all()
        if qres:
            for item in qres:
                res.append({
                    'course_id': item.course_id,
                    'matr_num': item.matr_num,
                    'year': item.year
                })
    if matr_num != None:
        qres = registrations.query.filter(registrations.matr_num.in_([matr_num])).all()
        if qres:
            for item in qres:
                tmp = {
                    'course_id': item.course_id,
                    'matr_num': item.matr_num,
                    'year': item.year
                }
                if tmp not in res:
                    res.append(tmp)
    return res

def get_course(course_id=None):
    res = None
    if course_id:
        qres = courses.query.filter(courses.course_id.in_([course_id])).first()
        res = {
            'course_id': qres.course_id,
            'year': qres.year,
            'prof_id': qres.prof_id,
            'name': qres.name
        }
    else:
        qres = courses.query.all()
        if qres:
            res = []
            for item in qres:
                res.append({
                    'course_id': item.course_id,
                    'year': item.year,
                    'prof_id': item.prof_id,
                    'name': item.name
                })
    return res

def get_chat(course_id=None):
    res = None
    if course_id:
        qres = chats.query.filter(chats.course_id.in_([course_id])).first()
        res = {
            'course_id': qres.course_id,
            'chat_id': qres.chat_id
        }
    else:
        qres = chats.query.all()
        if qres:
            res = []
            for item in qres:
                res.append({
                    'course_id': item.course_id,
                    'chat_id': item.chat_id
                })
    return res

def get_messages(chat_id):
    res = []
    qres = messages.query.filter(messages.chat_id.in_([chat_id])).all()
    if qres:
        for item in qres:
            student_sender = students.query.filter(students.matr_num.in_([item.sender])).first()
            res.append({
                'id': item.id,
                'chat_id': item.chat_id,
                'sender': item.sender,
                'sender_name': student_sender.first_name + ' ' + student_sender.last_name,
                'sent_time': item.sent_time.strftime('%H:%M'),
                'content': item.content
            }) 
    return res