from flask_app import app
from flask import render_template, redirect, request, session

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    session["name"] = request.form["name"]
    session["location"] = request.form["location"]
    session["language"] = request.form["language"]
    session["color"] = request.form["color"]
    session["pizza"] = request.form.getlist("pizza")
    session["comments"] = request.form["comments"]
    print(session["color"])
    return redirect("/result")

@app.route("/result")
def result():
    info = [("Name:", session["name"]), ("Dojo Location:", session["location"]), ("Favorite Language:", session["language"]), ("Favorite Color:", session["color"]), ("Pizza Types:", session["pizza"]), ("Comments:", session["comments"])]
    return render_template("result.html", info=info)