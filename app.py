from flask import Flask, render_template, request, jsonify, url_for, redirect
from backend.db import db
from backend.users import usersapp
from backend.auth import auth, login_required
from backend.mahasiswa import mahasiswa_fc



#membuat variable app bisa menggunakan class flask
app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = 'das2133'

app.register_blueprint(usersapp)
app.register_blueprint(auth)
app.register_blueprint(mahasiswa_fc) 

@app.route('/')
@login_required
def index():
    return render_template("index.html")

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         data = {
#             'username' : request.form['username'],
#             'password' : request.form['sandi']
#         }
#         return jsonify(data)
#     return render_template("login.html")


if __name__ == "__main__":
    app.run(debug = True, port=6006)