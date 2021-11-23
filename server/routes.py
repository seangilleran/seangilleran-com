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
    flask.g.html, flask.g.meta = data
    return flask.render_template("page.html")


@routes.app_context_processor
def inject_mungifier():
    def mungify(txt):
        out = ""
        for c in txt:
            out = out + random.choice([f"&#{ord(c)};", f"&#x{format(ord(c), 'x')};"])
        return out
    return dict(mungify=mungify)


@routes.route("/")
def index():
    return _render_page("_index")


@routes.route("/cv")
def cv():
    return _render_page("_cv")


@routes.route("/projects")
def projects():
    return _render_page("_projects")


@routes.route("/blog")
def blog():
    return flask.abort(404)
