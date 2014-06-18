from flask import Flask, request, render_template, url_for, redirect, session, request
from werkzeug.utils import secure_filename
import json, urllib, urllib2, utils, os
 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc'])
 
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['UPLOAD_FOLDER'] = '/uploads'
 
env = app.jinja_env
env.globals.update(utils=utils)
 
@app.route("/classes")
def classes():
    return render_template("class.html")
 
@app.route("/classes/<classname>")
def one_class():
    pass
 
@app.route("/addclass", methods=["GET", "POST"])
def add_class():
    return render_template("addclass.html")
 
 
@app.route("/")
def home():
    return render_template("home.html")
 
@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        return redirect(url_for("/"))
    if request.method == "GET":
        return render_template("register.html")
    elif "username" not in session:
        firstname = request.form["first"]
        lastname = request.form["last"]
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        if utils.register(username, password, firstname, lastname, email):
            session["username"] = username
            return redirect(url_for("profile"))
        else:
            return redirect(url_for("register"))
    else:
        return redirect(url_for("register"))
 
 
@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("home.html"))
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        if utils.login_user(username, password):
            return redirect(url_for("profile"))
        else:
            return redirect(url_for("home"))
 
@app.route("/logout")
def logout():
    utils.logout_user()
    return redirect(url_for('home'));
 
 
# Do we want to have a profile that shows what classes you are attached to?
@app.route("/profile")
def profile():
    classes = utils.get_classes(session["username"])
    return render_template("profile.html", username=session['username'], classes=classes)
 
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
