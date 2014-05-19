from flask import Flask, request, render_template, url_for, redirect, session, request
import json
import urllib,urllib2

import utils

app=Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'



@app.route("/")
def home():
        if "username" not in session:
                return render_template("login.html")
        else:
                return redirect("/")


@app.route("/register", methods = ["GET", "POST"])
def register():
        if "username" in session:
                return redirect(url_for("/"))
                if request.method == "GET":
                        return render_template("register.html")
                        if "username" not in session:
                                username = request.form["username"]
                                password = request.form["password"]
                                confirm = request.form["confirm"]
                                securityq = request.form["securityq"]
                                securitya = request.form["securitya"]
                                if utils.register(username, password, confirm, securityq, securitya):
                                        session["username"] = username
                                        return redirect(url_for("search"))
                                else:
                                        return redirect(url_for("register"))
        else:
                return redirect(url_for("search"))

        
@app.route("/login", methods = ["GET", "POST"])
def login():
        if "username" in session:
                return redirect(url_for("home.html"))
                if request.method == "GET":
                        return render_template("index.html")
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
        events = utils.getEvents(session["username"])
        return render_template("profile.html", username = session['username'], events = events)
        
    
@app.route("/addschool")
def addschool():
        if "username" in session: 
                schoolname = request.form["schoolname"]
                if schoolname == null:
                        return redirect("/addschool")
                else:
                        utils.addschool(session["username"], schoolname)
                        return render_template("school.html")
                        
        else:
                return redirect("/login")
                
@app.route("/addclass")
def addclass():
        if "username" in session:
                subject = request.form["subject"]
                classname = request.form["classname"]
                if (subject == null) or (classname == null):
                    return redirect("/addclass")
                else:
                    utils.addclass(session["username"], subject, classname)
                    return render_template("class.html")
        else:
            return redirect("/login")
                        
@app.route("/<Schoolname>")
def school():
        return render_template("school.html")

@app.route("/<Schoolname>/<Subject>/<Classname>")
def subject():
        return render_template("subject.html")

@app.route("/<Schoolname>/<Subject>/<Classname>")
def classname():
        return render_template("class.html")

@app.route("/<Schoolname>/<Subject>/<Classname>/addDoc")
def addDoc():  
        for f in request.files:
                file = request.files[f]
                filename=files.filename
                if (files[filename] == null):
                    file.save(filename)
                else: 
                    render_template("docerror.html")       
            
@app.route("/<Schoolname>/<Subject>/<Classname>/editDoc")
def editDoc():
    for f in request.files:
        file = request.files[f]
        filename=file.filename
        if (files[filename] == null):
            render_template("docerror2.html")
        else: 
            file.save(filename)

            
@app.route("/<Schoolname>/<Subject>/<Classname>/editDoc")
def editDoc():
        for f in request.files:
            file = request.files[f]
            qname=f
            filename=file.filename
            if (files[filename] == null):
               render_template("docerror.html")
            else: 
                file.save(filename)




if __name__=="__main__":
        app.debug=True
        app.run(host='0.0.0.0',port=5000)

