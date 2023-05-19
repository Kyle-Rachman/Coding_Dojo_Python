from flask import Flask, render_template

app = Flask(__name__)

@app.route("/play/")
def play():
    return render_template("index.html", times = 3, alignment = "center", color = "lightblue")

@app.route("/play/<int:x>")
def play_x_times(x):
    return render_template("index.html", times = x, alignment = "flex-start", color = "lightblue")

@app.route("/play/<int:x>/<string:color>")
def play_x_times_colored(x,color):
    return render_template("index.html", times = x, alignment = "flex-start", color = color)

if __name__ == "__main__":
    app.run(debug = True)