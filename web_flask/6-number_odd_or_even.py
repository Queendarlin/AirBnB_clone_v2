#!/usr/bin/python3
"""A script that starts a Flask web application"""

from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """Route that displays 'Hello HBNB!' """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Route that displays 'HBNB'"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """Route that displays 'C ' followed by the value of the text variable"""
    return f"C {escape(text.replace('_', ' '))}"


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text):
    """Route that displays 'Python ',
    followed by the value of the text variable """
    return f"Python {escape(text.replace('_', ' '))}"


@app.route('/number/<int:n>', strict_slashes=False)
def is_a_number(n):
    """Route that displays 'n is a number' only if n is an integer"""
    return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Route that displays an HTML page only if n is an integer"""
    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """Route that displays an HTML page only if n is an integer,
        showing if the number is odd or even"""
    if n % 2 == 0:
        even_or_odd = "even"
    else:
        even_or_odd = "odd"
    return render_template('6-number_odd_or_even.html', number=n, output=even_or_odd)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
