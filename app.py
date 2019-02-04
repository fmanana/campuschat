from flask import Flask, render_template, url_for
import os

app = Flask(__name__, template_folder=os.path.abspath('templates'), static_folder=os.path.abspath('static'))

@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

