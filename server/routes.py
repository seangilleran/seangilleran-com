""" routes.py
"""

import random

import flask

from server import db


routes = flask.Blueprint('routes', __name__)


def _render_page(name):

    data = db.get_page(name)
    if not data or data is None:
        return flask.abort(404)

    # We use flask.g to store data global to the application context. See:
    # https://flask.palletsprojects.com/en/2.0.x/appcontext/
    flask.g.html, flask.g.meta = data

    return flask.render_template("page.html")


@routes.route("/")
def index():
    return _render_page("index")


@routes.route("/cv")
def cv():
    return _render_page("cv")


@routes.route("/projects")
def projects():
    return _render_page("projects")


@routes.route("/blog")
def blog():
    # TODO
    return flask.abort(404)


@routes.app_context_processor
def inject_mungifier():

    def mungify(txt):

        # This is a small function to apply a light scramble to stuff we don't
        # want robots to find, like email addresses. It's not very secure!
        out = ""
        for c in txt:
            out = out + random.choice([f"&#{ord(c)};", f"&#x{format(ord(c), 'x')};"])
        return out

    return dict(mungify=mungify)
