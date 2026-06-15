#!/usr/bin/python3
"""Starts a Flask web application with /states and /states/<id> routes."""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy session."""
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """Display the list of all States, or one State and its Cities."""
    states = sorted(storage.all(State).values(), key=lambda s: s.name)

    if id is None:
        return render_template('9-states.html', states=states)

    state = None
    for s in states:
        if s.id == id:
            state = s
            break

    return render_template('9-states.html', state=state)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
