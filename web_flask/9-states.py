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


@app.route("/states/<id>", strict_slashes=False)
@app.route("/states", strict_slashes=False)
def states(id=None):
    """Fetch and render states."""
    state_objs = list()
    found_state = None
    for k, obj in storage.all(State).items():
        state_objs.append(obj)
        k_id = k.split('.')[1]
        if str(id) == k_id:
            found_state = obj

    return render_template(
        '9-states.html',
        states=state_objs,
        id_arg=id,
        found_state=found_state
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
