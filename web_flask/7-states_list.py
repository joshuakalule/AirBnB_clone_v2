#!/usr/bin/python3
""" starts a flask web application """
from flask import Flask, render_template
from markupsafe import escape
from models import storage
from models.state import State
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    """ Home page route """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb_home():
    """ Hbnb page route """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """ Sub directory c route """
    text = text.replace("_", " ")
    return f"C {escape(text)}"


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def py_route(text="is cool"):
    """ Sub directory python route """
    text = text.replace("_", " ")
    return f"Python {escape(text)}"


@app.route("/number/<int:n>", strict_slashes=False)
def number_route(n):
    """ Sub directory number route """
    return f"{escape(n)} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """ Sub directory number template route """
    return render_template('5-number.html', n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def odd_or_even(n):
    """ Sub directory number template route II """
    return render_template('6-number_odd_or_even.html', n=n)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """ States list route """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=sorted_states)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ Teardown app context """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
