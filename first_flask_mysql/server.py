from flask_app.controllers import friends
from flask_app import app

if __name__ == "__main__":
    app.run(debug=True)

# set debug to False when deployed