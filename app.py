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
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
from flask import Flask, request, render_template, url_for, redirect, session, request
import json
import urllib
import urllib2
 
import utils
 
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
 
 
@app.route("/")
def home():
    return render_template("home.html", loggedIn=utils.logged_in())
 
 
@app.route("/about")
def about():
    return render_template("index.html")
 
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
    classes = utils.getClasses(session["username"])
    return render_template("profile.html", username=session['username'], classes=classes)
 
 
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
        filename = file.filename
        if (file[filename] is None):
            file.save(filename)
        else:
            render_template("docerror.html")
 
 
@app.route("/schools/<Schoolname>/<Subject>/<Classname>/editDoc")
def editDoc():
    for f in request.files:
        file = request.files[f]
        qname = f
        filename = file.filename
        if (file[filename] is None):
            render_template("docerror2.html")
        else:
            file.save(filename)
 
 
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
