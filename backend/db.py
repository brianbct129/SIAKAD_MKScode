
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyAMa1BmkfsoAu3k0KISuKi8un-RAX970Kc",
    "authDomain": "belajarflask-71d20.firebaseapp.com",
    "databaseURL": "https://belajarflask-71d20-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "belajarflask-71d20",
    "storageBucket": "belajarflask-71d20.appspot.com",
    "messagingSenderId": "778816380397",
    "appId": "1:778816380397:web:609462f7f873c7c5925be4"
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def get_all_collection(collection, orderBy=None, direction=None):
    if orderBy:
        collects_ref = db.collection(collection).order_by(
            orderBy, direction=direction)
    else:
        collects_ref = db.collection(collection)
    collects = collects_ref.stream()
    RETURN = []
    for collect in collects:
        ret = collect.to_dict()
        ret['id'] = collect.id
        RETURN.append(ret)
    return RETURN



