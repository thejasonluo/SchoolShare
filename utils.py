from pymongo import MongoClient
from flask import session
 
client = MongoClient()
db = client.schoolshare
 
def record_exists(collection, query, limit=1):
    return collection.find(query, limit=1).count(True) > 0
 
def user_exists(username):
    return record_exists(db.users, {'username': username})
 
def authorize(username, password):
    return record_exists(db.users, {'username': username, 'password': password})
 
def update_user(username, password):
    db.users.update(
        {'username': username},
        {'password': password},
        upsert=True
    )
 
 
def insert_user(username, password, first, last, email):
    db.users.insert(
        {'username': username,
         'password': password,
         'first': first,
         'last': last,
         'email': email,
         'classes': [],
         }
    )
 
def login_user(username, password):
    if authorize(username, password):
        session['username'] = username
        return True
    else:
        return False
 
def logout_user():
    session.pop('username', None)
 
def register(username, password, first, last, email):
    if (user_exists(username)):
        return 'User Already Exists.'
    else:
        insert_user(username, password, first, last, email)
        login_user(username, password)
        return 'Success!'
 
def change_password(username, password):
    if (len(password) < 4):
        return 'Password too short.'
    else:
        update_user(username, password)
        return 'Success!'
 
def change_username(username, new_username):
    db.users.update({'username': username}, {'username': new_username})
 
 
def logged_in():
    if not user_exists(session.get('username', None)):
        session.pop('username', None)
    return session.get('username', None) != None
 
def add_class(username, classname):
    db.classes.insert({"name": classname, "user": username})
 
def get_classes(username):
    return db.classes.find({"user": username})
