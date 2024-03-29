from flask_app import app
from flask import render_template, redirect, request, session, url_for
from flask_app.models.dojo import Dojo
from flask_app.models.ninja import Ninja

@app.route("/")
def root():
    return redirect("/dojos")

@app.route("/dojos")
def dojos():
    dojos = Dojo.get_all()
    return render_template("dojos.html", dojos = dojos)

@app.route("/createdojo", methods=["POST"])
def create_dojo():
    data = {"name" : request.form["name"]}
    Dojo.save_dojo(data)
    return redirect("/dojos")

@app.route("/dojos/<int:x>")
def dojo_info(x):
    dojo = Dojo.get_one(x)
    data = {
        "id" : dojo.id
    }
    ninjas = Dojo.get_dojo_ninjas(data)
    return render_template("dojo_info.html", dojo = dojo, ninjas = ninjas)

@app.route("/deleteninja/<int:id>/<int:dojo_id>")
def delete_ninja(id, dojo_id):
    ninja_id = id
    dojo_id = dojo_id
    Ninja.destroy_ninja(ninja_id)
    return redirect(url_for('dojo_info', x = dojo_id))