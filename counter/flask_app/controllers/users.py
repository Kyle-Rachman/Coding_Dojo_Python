from flask_app import app
from flask import render_template, redirect, request, session,url_for

@app.route("/", defaults={"visitnum":1})
@app.route("/<int:visitnum>")
def index(visitnum):
    if "visited" in session:
        session["visits"] += visitnum
        session["truevisits"] += 1
    else:
        session["visited"] = True
        session["visits"] = 1
        session["truevisits"] = 1
    return render_template("index.html")

@app.route("/destroy_session")
def destroy():
    session.clear()
    return redirect("/")

@app.route("/incrementform", methods=["POST"])
def increment():
    num = request.form['visitnum']
    return redirect(url_for('index', visitnum=num))
