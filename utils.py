1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
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
         'subjects': []}
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
 
 
def addSchool(username, school):
    db.users.update(
        {"username": username}, {'$set': {'school': school}})
    return school
 
 
def addSubject(username, subject, classes):
    db.users.update({"username": username}, {'$push': {'subjects': subject}})
    return subject
 
 
def addClass(username, subject, classname):
    db.users.update({"username": username}, {'$push': {'subjects': subject, "classes": classname}})
    return classname
 
 
def getClasses(username):
    classes = [x for classes in db.users.find({"username": username})]
    return classes
