from pymongo import MongoClient
from flask import session

client = MongoClient()
db = client.users

def register(username, password, first, last, email):
	if db.Collections.find_one({"username":username}) is None:
		db.Collections.insert({"username":username, "password": password, "first": first, "last": last, "email": email, "classes": [], "subjects": []})
		return True
	else:
		return False


def authorize(username, password):
	user = db.Collections.find_one({"username": username, "password": password})
	if user:
		return True
	else:
		return False

def loggedIn():
	if "username" in session:
		return True
	else:
		session["error"] = "mustLogin"
		return False
		
		
def addSchool(username, school):
	db.Collections.update({"username": username}, {'$set' : {'school': school}})
	return school
		
def addSubject(username, subject, classes):
	db.Collections.update({"username":username}, {'$push': {'subjects' : subject}})
	return subject
	
def addClass(username, subject, classname):
	db.Collections.update({"username":username}, {'$push': {'subjects': subject, "classes": classname}})
	return classname


def getClasses(username):
	classes = [x for classes in db.Collections.find({"username": username})]
	return classes


