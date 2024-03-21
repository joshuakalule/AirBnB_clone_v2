#!/usr/bin/python3
""" starts a flask web application """
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    """ Home page route """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb_home():
    """ Hbnb page route """
    return "HBNB"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
