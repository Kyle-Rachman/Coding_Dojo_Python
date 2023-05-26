from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def render_std_board():
    return render_template("index.html", rows = 8, cols = 8, dark_color = "black", light_color = "red")

@app.route("/<int:x>")
def render_board_var_rows(x):
    return render_template("index.html", rows = x, cols = 8, dark_color = "black", light_color = "red")

@app.route("/<int:x>/<int:y>")
def render_board_var_rows_var_cols(x,y):
    return render_template("index.html", rows = x, cols = y, dark_color = "black", light_color = "red")

@app.route("/<int:x>/<int:y>/<string:color1>/<string:color2>")
def render_board_var_rows_var_cols_var_colors(x,y,color1,color2):
    return render_template("index.html", rows = x, cols = y, dark_color = color1, light_color = color2)

if __name__ == "__main__":
    app.run(debug = True)