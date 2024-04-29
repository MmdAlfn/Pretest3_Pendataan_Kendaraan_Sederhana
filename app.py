from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
from bson import ObjectId
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def pendataan():
    return render_template('pendataan.html')

@app.route('/pendataan', methods=['GET', 'POST'])
def pendataan_new():
    return render_template('pendataan.html')

@app.route('/detail', methods=['GET', 'POST'])
def detail():
    
    if request.method=='POST':
        jenis = request.form['jenis_kendaraan']
        merk = request.form['merk_kendaraan']
        plat = request.form['plat_kendaraan']
            
        doc = {
            'jenis': jenis,
            'merk': merk,
            'plat': plat
        }
                
        db.kendaraan.insert_one(doc)
                
        return redirect(url_for('detail'))
    
    datas = list(db.kendaraan.find({}))
    return render_template('detail.html', datas=datas)

@app.route('/deletekendaraan/<_id>', methods=['GET', 'POST'])
def deletekendaraan(_id):
    id = ObjectId(_id)
    db.kendaraan.delete_one({'_id': id})
    return redirect(url_for('pendataan'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)