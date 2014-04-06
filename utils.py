from pymongo import MongoClient
from flask import session

def register(username, password, first, last, school):
	db=getDB()
	if db.Collections.find_one({"username":username}) is None:
		db.Collections.insert({"username":username, "password": password, "first": first, "last": last, "school", school})
		return True
	else:
		return False


def getDB():
	client = MongoClient()
	db = client.users
	return db

def authorize(username, password):
	db= getDB()
	user = db.Collections.find_one({"useername": username, "password": password})
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
		