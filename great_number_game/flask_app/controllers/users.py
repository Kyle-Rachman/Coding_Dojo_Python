from flask_app import app
from flask import render_template, redirect, request, session
import random



@app.route("/")
def index():
    if "rand_number" not in session:
        session["rand_number"] = random.randint(1, 100)
        session["guesses"] = 0
        session["show_result"] = "none"
        session["show_guess"] = "none"
    return render_template("index.html")

@app.route("/guess", methods = ["POST"])
def guess():
    guessed_num = int(request.form["guess-num"])
    session["guesses"] += 1
    session["show_guess"] = "flex"
    if guessed_num > session["rand_number"]:
        session["status"] = "Too high!"
        session["color"] = "red"
    elif guessed_num < session["rand_number"]:
        session["status"] = "Too low!"
        session["color"] = "red"
    else:
        session["status"] = f"{guessed_num} was the number!"
        session["show_result"] = "block"
        session["color"] = "green"
    return redirect("/")

@app.route("/reset")
def reset():
    session.clear()
    return redirect("/")