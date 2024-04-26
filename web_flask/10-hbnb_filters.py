#!/usr/bin/python3
"""Starts a flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
app = Flask(__name__)


@app.teardown_appcontext
def close(error):
    """Removes the current SQLAlchemy Session."""
    storage.close()


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """Fetch and render states with their cities, and ammenities."""
    amenities = list(storage.all(Amenity).values())
    states = list(storage.all(State).values())

    return render_template(
        "10-hbnb_filters.html",
        amenities=amenities,
        states=states
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
