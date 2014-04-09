from pymongo import MongoClient
from flask import session

def register(username, password, first, last, school):
	db=getDB()
	if db.Collections.find_one({"username":username}) is None:
		db.Collections.insert({"username":username, "password": password, "first": first, "last": last, "school": school, "classes": []})
		return True
	else:
		return False


def getDB():
	client = MongoClient()
	db = client.users
	return db

def authorize(username, password):
	db= getDB()
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
	db = getDB()
	db.update({"username": username}, {'$set' : {'school': school}})
	return school
		
def addClass(username, classname):
	db=getDB()
	db.update({"username":username}, {'$push': {'classes' : classname}})
	return classname
	
#def getClassmates(school, classname):
#	db = getDB()
# figure out how to query in MongoDB
	
