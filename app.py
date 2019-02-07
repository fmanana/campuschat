from flask import Flask, flash, request, render_template, redirect, session, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_socketio import SocketIO, send
import os
import string
import random
from db.tables import *


engine = create_engine('sqlite:///db/campuschat.db', echo=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/campuschat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'b\xd0~R;\xaa=\xd2\nv\xb4\xf2M\x06\x13ok'
db = SQLAlchemy(app)
socketio = SocketIO(app)

def generate_random(n=64):
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(n))

@app.route('/index')
@app.route('/home')
@app.route('/')
def home():
    if session.get('matr_num'):
        return redirect(url_for('chat'))
    else:
        return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/imprint')
def imprint():
    return render_template('imprint.html')

@app.route('/contact-us')
def contact_us():
    return render_template('contact-us.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    post_username = str(request.form['username'])
    post_password = str(request.form['password'])

    random_token = generate_random()
    print(random_token)
    session[random_token] = {
        'username': post_username,
        'password': post_password
    }

    return redirect(url_for('login_auth', token=random_token))

@app.route('/login-auth/<token>')
def login_auth(token):
    if not session[token]:
        return redirect(url_for('home'))
    post_username = session[token]['username']
    post_password = session[token]['password']
    session.pop(token, None)

    Session = sessionmaker(bind=engine)
    s = Session()

    result = s.query(auth).filter(auth.email.in_([post_username]), auth.password.in_([post_password])).first()
    if result:
        student_query = s.query(students).filter(students.email.in_([post_username])).first()
        session['logged_in'] = True
        session['matr_num'] = student_query.matr_num
        return redirect(url_for('chat'))
    else:
        return redirect(url_for('home'))

@app.route('/chat', defaults={'course_id': None})
@app.route('/chat/<course_id>')
def chat(course_id):
    if session.get('matr_num'):
        user_registrations = get_registrations(matr_num=session['matr_num'])
        user_courses = [get_course(x['course_id']) for x in user_registrations]
        user_chats = [get_chat(x['course_id']) for x in user_courses]
        user_data = get_student_by_id(session['matr_num'])
        user_messages = []
        course_name = 'CampusChat'
        active_chat_id = None
        if course_id:
            for item in user_courses:
                if course_id == item['course_id']:
                    course_name = item['name']
                    break
            active_chat_id = chats.query.filter(chats.course_id.in_([course_id])).first().chat_id
            user_messages = get_messages(active_chat_id)
            print(user_messages)
        return render_template('chat.html', registrations=user_registrations, chats=user_chats, courses=user_courses,\
            messages=user_messages, course_name=course_name, active_chat_id=active_chat_id, user_data=user_data, matr_num=session['matr_num'])
    else:
        return redirect(url_for('home'))

@app.route('/chat/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('matr_num', None)
    return redirect(url_for('home'))

@socketio.on('message')
def handle_message(msg, chat_id):
    if session.get('matr_num'):
        new_row = messages(chat_id=chat_id, sender=session['matr_num'], content=msg)
        db.session.add(new_row)
        db.session.commit()
        send(msg, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
    # app.run(debug=True, port='5000')


# API



