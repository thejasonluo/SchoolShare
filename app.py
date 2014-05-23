from flask import Flask, request, render_template, url_for, redirect, session, request
import json
import urllib,urllib2

import utils

app=Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'



@app.route("/")
def home():
        return render_template("home.html")


@app.route("/register", methods = ["GET", "POST"])
def register():
        if "username" in session:
                return redirect(url_for("/"))
        if request.method == "GET":
                return render_template("register.html")
        elif "username" not in session:
                username = request.form["username"]
                password = request.form["password"]
                confirm = request.form["confirm"]
                firstname = request.form["first"]
                lastname = request.form["securitya"]
                school = request.form["school"]
                if password == confirm:
                        if utils.register(username, password, firstname, lastname, school):
                                session["username"] = username
                                return redirect(url_for("search"))
                        else:
                                return redirect(url_for("register"))
        else:
                return redirect(url_for("register"))
        
@app.route("/login", methods = ["GET", "POST"])
def login():
        if "username" in session:
                return redirect(url_for("home.html"))
        if request.method == "GET":
                return render_template("login.html")
        else:
                username = request.form["username"]
                password = request.form["password"]
                if utils.authorize(username, password):
                        session["username"] = username
                        return redirect(url_for("search"))
                else:
                        return redirect(url_for("login"))

@app.route("/logout")
def logout():
        session.pop("username",None)
        return redirect("/")

        


##Do we want to have a profile that shows what classes you are attached to?

@app.route("/profile")
def profile():
        classes = utils.getClasses(session["username"])
        return render_template("profile.html", username = session['username'], classes = classes)
        
    
@app.route("/addschool")
def addschool():
        if "username" in session: 
                schoolname = request.form["schoolname"]
                if schoolname is None:
                        return redirect("/addschool")
                else:
                        utils.addSchool(session["username"], schoolname)
                        return render_template("school.html")
                        
        else:
                return redirect("/login")
                
@app.route("/addclass")
def addclass():
        if "username" in session:
                subject = request.form["subject"]
                classname = request.form["classname"]
                if (subject is None) or (classname is None):
                        return redirect("/addclass")
                else:
                        utils.addclass(session["username"], subject, classname)
                        return render_template("class.html")
        else:
                return redirect("/login")
                        
@app.route("/schools/<Schoolname>")
def school():
        return render_template("school.html")

@app.route("/schools/<Schoolname>/<Subject>/<Classname>")
def subject():
        return render_template("subject.html")

@app.route("/schools/<Schoolname>/<Subject>/<Classname>")
def classname():
        return render_template("class.html")

@app.route("/schools/<Schoolname>/<Subject>/<Classname>/addDoc")
def addDoc():  
        for f in request.files:
                file = request.files[f]
                filename=file.filename
                if (file[filename] is None):
                        file.save(filename)
                else: 
                        render_template("docerror.html")       
                        

            
@app.route("/schools/<Schoolname>/<Subject>/<Classname>/editDoc")
def editDoc():
        for f in request.files:
                file = request.files[f]
                qname=f
                filename=file.filename
                if (file[filename] is None):
                        render_template("docerror2.html")
                else: 
                        file.save(filename)




if __name__=="__main__":
        app.debug=True
        app.run(host='0.0.0.0',port=5000)

