from flask import Blueprint, redirect, render_template, url_for, jsonify, flash, request, session
from werkzeug.security import check_password_hash
from backend.db import db, get_all_collection
from functools import wraps

auth = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash('Anda harus login', 'danger')
            return redirect(url_for('auth.login'))
    return wrapper

#login
@auth.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        cek_username = db.collection('users').where('username', '==', username).stream()
        user = {}

        for ck in cek_username:
            user = ck.to_dict()
            user['id'] = ck.id

        if user:
            if check_password_hash(user['password'], password):
                # return "password benar"\
                session['user'] = user
                flash('berhasil login', "success")
                return redirect(url_for('index'))
            else:
                # return "password salah"
                flash('password salah', "danger")
                return redirect(url_for('.login'))
        else:
            flash("User tidak terdaftar", "danger")
            return redirect(url_for('.login'))
    if 'user' in session:
        flash('anda sudah login', "warning")
        return redirect(url_for('index'))
    
    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.clear()
    flash('Berhasil Logout', 'success')
    return redirect(url_for('.login'))

@auth.route('/coba')
def coba():
    return session['user']