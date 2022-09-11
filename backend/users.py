from flask import Flask, Blueprint, render_template,url_for,redirect, jsonify, request, flash
from backend.db import db, get_all_collection
from werkzeug.security import generate_password_hash
from backend.auth import login_required

usersapp = Blueprint('usersapp', __name__)


#menu crud
@usersapp.route('/users')
@login_required
def users():
    users = get_all_collection('users')
    return render_template('users/users.html', users = users)

#create
@usersapp.route('/users/tambah', methods=['POST', 'GET'])
@login_required
def users_tambah():
    if request.method == 'POST':
        if request.form["Password"] != request.form["Password_1"]:
            flash ("Password tidak sama", 'danger')
            return redirect(url_for("usersapp.users_tambah"))

        lihat_pengguna = db.collection('users').where('username', '==', request.form['Username']).stream()
        pengguna = {}
        for p in lihat_pengguna:
            user = p.to_dict()
            pengguna = user
        
        if pengguna:
            flash('Username Sudah ada', 'danger')
            return redirect(url_for("usersapp.users_tambah"))
        else:    
            # untuk input 
            data ={
                'nama_lengkap': request.form['nama_lengkap'],
                'username': request.form['Username'],
                'email': request.form['Email'],
            }
            data['password'] = generate_password_hash(request.form['Password'], 'sha256')
            db.collection('users').document().set(data)
            return redirect (url_for('.users'))
            # return jsonify(data)
    return render_template('users/tambah_users.html')

#update
@usersapp.route('/users/edit/<uid>', methods=['POST', 'GET'])
@login_required
def users_edit(uid):
    if request.method == "POST":
        data ={
                'nama_lengkap': request.form['nama_lengkap'],
                'email': request.form['Email'],
            }
        db.collection('users').document(uid).update(data)
        return redirect (url_for('.users'))
    data = db.collection('users').document(uid).get().to_dict()
    return render_template('users/edit_users.html', data=data)

#delete
@usersapp.route('/users/delete/<uid>')
@login_required
def user_delete(uid):
    db.collection('users').document(uid).delete()
    flash("data berhasil di hapus", "danger")
    return redirect (url_for('.users'))

#Read
@usersapp.route('/users/lihat/<uid>')
@login_required
def lihat_users(uid):
    data = db.collection('users').document(uid).get().to_dict()
    return render_template('users/lihat_users.html', data=data)

