#!/usr/bin/python3
""" Cities by States Module for HBNB project """

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def list_states():
    """ Display a list of states sorted by name """
    states = storage.all(State).values()
    states_sorted = sorted(states, key=lambda x: x.name)
    return render_template('9-states.html', states=states_sorted)
@app.route('/states/<id>', strict_slashes=False)
def state_id():


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
