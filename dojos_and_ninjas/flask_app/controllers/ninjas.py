from flask_app import app
from flask import render_template, redirect, request, session, url_for
from flask_app.models.dojo import Dojo
from flask_app.models.ninja import Ninja

@app.route("/ninjas")
def ninjas():
    dojos = Dojo.get_all()
    return render_template("create_ninja.html", dojos = dojos)

@app.route("/createninja", methods=["POST"])
def create_ninja():
    data = {
        "dojo" : int(request.form["dojo"]),
        "fname" : request.form["fname"],
        "lname" : request.form["lname"],
        "age" : int(request.form["age"])
    }
    Ninja.save_ninja(data)
    return redirect(url_for("dojo_info", x = data["dojo"]))