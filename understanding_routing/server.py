from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/dojo")
def dojo():
    return "Dojo!"

@app.route("/say/<string:name>")
def say(name):
    return f"Hi {name}!"

@app.route("/repeat/<int:num>/<string:word>")
def repeat(num,word):
    return f"{word * num}"

@app.route("/<undefined>")
def error(undefined):
    return "Sorry! No response. Try again."

if __name__ == "__main__":
    app.run(debug = True)