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


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """Fetch and render states."""
    state_objs = list()
    for k, obj in storage.all(State).items():
        state_objs.append(obj)

    return render_template('8-cities_by_states.html', states=state_objs)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
