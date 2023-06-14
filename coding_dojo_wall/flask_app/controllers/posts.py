from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.post import Post

@app.route("/make_post", methods=['POST'])
def make_post():
    data = {
        "content" : request.form["content"],
        "user" : session["user_id"]
    }
    if not Post.validate_post(data):
        return redirect("/wall")
    
    Post.save(data)
    return redirect("/wall")

@app.route("/delete_post", methods=['POST'])
def delete_post():
    data = {
        "id" : request.form["post_id"]
    }
    Post.delete(data)
    return redirect("/wall")