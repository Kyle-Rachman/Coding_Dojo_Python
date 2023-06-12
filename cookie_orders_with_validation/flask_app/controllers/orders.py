from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.order import Order


@app.route("/")
def index():
    return redirect("/cookies")

@app.route("/cookies")
def cookies():
    orders = Order.get_all()
    return render_template("cookies.html", orders = orders)

@app.route("/cookies/new")
def new_order():
    return render_template("new_order.html")

@app.route("/new/process", methods=["POST"])
def new_process():
    data = {
        "name" : request.form["name"],
        "type" : request.form["type"],
        "number" : request.form["number"]
    }
    if not Order.validate_order(data):
        return redirect("/cookies/new")
    
    Order.save(data)
    return redirect("/cookies")

@app.route("/cookies/edit/<int:x>")
def edit_order(x):
    order = Order.get_one(x)
    return render_template("change_order.html", order = order)

@app.route("/edit/process", methods=["POST"])
def edit_process():
    data = {
        "id" : request.form["id"],
        "name" : request.form["name"],
        "type" : request.form["type"],
        "number" : request.form["number"]
    }
    if not Order.validate_order(data):
        return redirect(url_for("edit_order", x = data["id"]))

    Order.update(data)
    return redirect("/cookies")