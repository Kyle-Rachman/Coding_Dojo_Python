from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_bcrypt import Bcrypt
from datetime import datetime
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/wall")
def wall():
    if "user_id" not in session:
        return redirect("/logout")
    user = User.get_one(session["user_id"])
    posts = Post.get_all_date_sorted()
    for post in posts:
        post.user = str(User.get_one(post.users_id).first_name) + " " + str(User.get_one(post.users_id).last_name)
        post.comments = Post.get_post_comments_date_sorted(post.id)
        post.created_at = post.created_at.strftime('%B %d')
        for comment in post.comments:
            if comment.users_id != None:
                comment.user = str(User.get_one(comment.users_id).first_name) + " " + str(User.get_one(comment.users_id).last_name)
                comment.created_at = comment.created_at.strftime('%B %d')
    return render_template("wall.html", user = user, posts = posts)

@app.route("/register", methods=['POST'])
def register():
    data = {
        "fname" : request.form["first_name"],
        "lname" : request.form["last_name"],
        "email" : request.form["email"],
        "pword" : request.form["password"],
        "confirm" : request.form["confirm"]
    }
    if not User.validate_user(data):
        return redirect("/")
    data["pword"] = bcrypt.generate_password_hash(data["pword"])
    user_id = User.save(data)
    session["user_id"] = user_id

    return redirect("/wall")

@app.route("/login", methods=['POST'])
def login():
    data = {
        "email" : request.form["email"]
    }

    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid email", "login")
        return redirect("/")
    
    if not bcrypt.check_password_hash(user_in_db.password,request.form["password"]):
        flash("Incorrect password!", "login")
        return redirect("/")

    session["user_id"] = user_in_db.id

    return redirect("/wall")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")