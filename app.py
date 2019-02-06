from flask import Flask, flash, request, render_template, redirect, session, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.tables import *
import os

engine = create_engine('sqlite:///db/campuschat.db', echo=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/campuschat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'b\xd0~R;\xaa=\xd2\nv\xb4\xf2M\x06\x13ok'
db = SQLAlchemy(app)

@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    return render_template('home.html')

<<<<<<< HEAD
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/imprint')
def imprint():
    return render_template('imprint.html')

@app.route('/contact-us')
def contact_us():
    return render_template('contact-us.html')
=======
@app.route('/login', methods=['POST', 'GET'])
def login():
    post_username = str(request.form['username'])
    post_password = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(auth).filter(auth.email.in_([post_username]), auth.password.in_([post_password]))
    result = query.first()
    if result:
        session['logged_in'] = True
        return render_template('chat.html')
    else:
        flash('Invalid username or password')
        return home()


>>>>>>> login

if __name__ == '__main__':
    app.run(debug=True, port=5000)

