from flask import Flask, flash, request, render_template, redirect, session, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_socketio import SocketIO, send
from db.tables import *
import os
import services.api as api

engine = create_engine('sqlite:///db/campuschat.db', echo=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/campuschat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'b\xd0~R;\xaa=\xd2\nv\xb4\xf2M\x06\x13ok'
db = SQLAlchemy(app)
socketio = SocketIO(app)

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

    random_token = api.generate_random()
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

@app.route('/chat')
def chat():
    if session.get('matr_num'):
        return render_template('chat.html')
    else:
        return redirect(url_for('home'))

@app.route('/chat/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('matr_num', None)
    return redirect(url_for('home'))

@socketio.on('message')
def handleMessage(msg):
    send(msg, broadcast=True)


if __name__ == '__main__':
    # app.run(debug=True, port=5000)
    socketio.run(app)

