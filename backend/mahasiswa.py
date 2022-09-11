from flask import Flask, Blueprint, render_template,url_for,redirect, jsonify, request, flash
from backend.db import db, get_all_collection, storage
from backend.auth import login_required


mahasiswa_fc = Blueprint('mahasiswa_fc', __name__)

@mahasiswa_fc.route('/data_mahasiswa')
@login_required
def mahasiswa():
    daftar_mahasiswa = db.collection("mahasiswa").stream()
    mahasiswa = []
    for mhs in daftar_mahasiswa:
        user = mhs.to_dict()
        user['id'] = mhs.id
        mahasiswa.append(user)
    return render_template("mahasiswa/data_mahasiswa.html",mahasiswa=mahasiswa)

@mahasiswa_fc.route('/tambah_mahasiswa', methods = ['POST', 'GET'])
@login_required
def tambah_mhs():
    if request.method == 'POST':
        data = {
            'nama_lengkap': request.form['nama_lengkap'],
            'email': request.form['email'],
            'jurusan': request.form['jurusan'],
            'umur': request.form['umur'],
            'status': 'lulus'
        }
        if 'image' in request.files and request.files['image']:
            image = request.files['image']
            ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
            filename = image.filename
            lokasi = f"mahasiswa/{filename}"
            ext = filename.rsplit('.', 1)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                storage.child(lokasi).put(image)
                data['photoURL'] = storage.child(lokasi).get_url(None)
            else:
                flash("Foto tidak diperbolehkan", "danger")
                return redirect(url_for('.tambah_mahasiswa'))
        db.collection('mahasiswa').document().set(data)
        return redirect(url_for("mahasiswa_fc.mahasiswa"))
        # return jsonify(data)
    return render_template("mahasiswa/tambah_mahasiswa.html")