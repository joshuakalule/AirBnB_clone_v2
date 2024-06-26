#!/usr/bin/python3
"""Starts a flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.teardown_appcontext
def close(error):
    """Removes the current SQLAlchemy Session."""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states():
    """Fetch and render states."""
    state_objs = list()
    for k, obj in storage.all(State).items():
        state_objs.append(obj)

    return render_template('7-states_list.html', states=state_objs)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
