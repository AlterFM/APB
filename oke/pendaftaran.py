from flask import Flask, render_template, request, redirect
from conndb import conndb
import json

app = Flask(__name__)

# Inisialisasi objek conndb
db = conndb()

# Fungsi untuk mendapatkan ID berikutnya
def get_next_id():
    strsql = "SELECT MAX(id) FROM tbl_pendaftaran"
    result = db.queryResult(strsql)
    if result[0][0] is not None:
        return result[0][0] + 1
    else:
        return 1

# Halaman utama - Menampilkan data pendaftaran dalam tabel
@app.route('/')
def index():
    strsql = 'SELECT * FROM tbl_pendaftaran'
    pendaftaran = db.queryResult(strsql)
    return render_template('index.html', pendaftaran=pendaftaran)
@app.route('/static/css/style.css')  # Rute baru untuk file CSS
def style():
    return app.send_static_file('css/style.css')


# Halaman tambah pendaftaran
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        tgl_pendaftaran = request.form['tgl_pendaftaran']
        nama = request.form['nama']
        alamat = request.form['alamat']
        telp = request.form['telp']
        jenis_kelamin = request.form['jenis_kelamin']
        jenis_kursus = request.form['jenis_kursus']

        next_id = get_next_id()

        strsql = "INSERT INTO tbl_pendaftaran (id, tgl_pendaftaran, nama, alamat, telp, jenis_kelamin, jenis_kursus) VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}')".format(next_id, tgl_pendaftaran, nama, alamat, telp, jenis_kelamin, jenis_kursus)
        db.queryExecute(strsql)

        return redirect('/')

    return render_template('add.html')

# Halaman edit pendaftaran
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        tgl_pendaftaran = request.form['tgl_pendaftaran']
        nama = request.form['nama']
        alamat = request.form['alamat']
        telp = request.form['telp']
        jenis_kelamin = request.form['jenis_kelamin']
        jenis_kursus = request.form['jenis_kursus']

        strsql = "UPDATE tbl_pendaftaran SET tgl_pendaftaran='{}', nama='{}', alamat='{}', telp='{}', jenis_kelamin='{}', jenis_kursus='{}' WHERE id={}".format(tgl_pendaftaran, nama, alamat, telp, jenis_kelamin, jenis_kursus, id)
        db.queryExecute(strsql)

        return redirect('/')

    strsql = "SELECT * FROM tbl_pendaftaran WHERE id={}".format(id)
    result = db.queryResult(strsql)
    if len(result) > 0:
        pendaftaran = result[0]
        return render_template('edit.html', pendaftaran=pendaftaran)
    else:
        return redirect('/')
    
# Rute untuk pembaruan data
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    tgl_pendaftaran = request.form['tanggal']
    nama = request.form['nama']
    alamat = request.form['alamat']
    telp = request.form['telepon']
    jenis_kelamin = request.form['jenis_kelamin']
    jenis_kursus = request.form['jenis_kursus']

    strsql = "UPDATE tbl_pendaftaran SET tgl_pendaftaran='{}', nama='{}', alamat='{}', telp='{}', jenis_kelamin='{}', jenis_kursus='{}' WHERE id={}".format(tgl_pendaftaran, nama, alamat, telp, jenis_kelamin, jenis_kursus, id)
    db.queryExecute(strsql)

    return redirect('/')

# Menghapus pendaftaran
@app.route('/delete/<int:id>')
def delete(id):
    strsql = "DELETE FROM tbl_pendaftaran WHERE id={}".format(id)
    db.queryExecute(strsql)

    return redirect('/')

# Fungsi untuk mendapatkan data pendaftaran dalam format JSON
@app.route('/get_json')
def get_json():
    strsql = 'SELECT * FROM tbl_pendaftaran'
    pendaftaran = db.queryResult(strsql)

    # Mengonversi data dari bentuk list-of-tuples ke bentuk list-of-dictionaries
    pendaftaran_json = []
    for p in pendaftaran:
        pendaftaran_json.append({
            'id': p[0],
            'tanggal_pendaftaran': p[1],
            'nama': p[2],
            'alamat': p[3],
            'telepon': p[4],
            'jenis_kelamin': p[5],
            'jenis_kursus': p[6]
        })

    return json.dumps(pendaftaran_json)

# Fungsi untuk pencarian data pendaftaran berdasarkan kriteria
@app.route('/search_json', methods=['POST'])
def search_json():
    keyword = request.form['keyword']

    # Query untuk mencari data berdasarkan kriteria
    strsql = "SELECT * FROM tbl_pendaftaran WHERE nama LIKE '%{}%' OR alamat LIKE '%{}%' OR jenis_kursus LIKE '%{}%'".format(keyword, keyword, keyword)
    pendaftaran = db.queryResult(strsql)

    # Mengonversi data dari bentuk list-of-tuples ke bentuk list-of-dictionaries
    pendaftaran_json = []
    for p in pendaftaran:
        pendaftaran_json.append({
            'id': p[0],
            'tanggal_pendaftaran': p[1],
            'nama': p[2],
            'alamat': p[3],
            'telepon': p[4],
            'jenis_kelamin': p[5],
            'jenis_kursus': p[6]
        })

    return json.dumps(pendaftaran_json)



if __name__ == '__main__':
    app.run(debug=True)
