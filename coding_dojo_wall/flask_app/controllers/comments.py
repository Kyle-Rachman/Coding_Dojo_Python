from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.comment import Comment

@app.route("/comment", methods=['POST'])
def make_comment():
    data = {
        "content" : request.form["comment-content"],
        "post" : request.form["post-num"],
        "user" : session["user_id"]
    }
    if not Comment.validate_comment(data):
        return redirect("/wall")
    
    Comment.save(data)
    return redirect("/wall")

@app.route("/delete_comment", methods=['POST'])
def delete_comment():
    data = {
        "id" : request.form["comment_id"]
    }
    Comment.delete(data)
    return redirect("/wall")