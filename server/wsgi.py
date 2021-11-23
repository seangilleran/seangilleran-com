""" app.py
"""

import secrets
import os

from flask import Flask

from server.routes import routes


def create_app(*args, **kwargs):

    app = Flask(
        __name__,
        template_folder=os.getenv("TEMPLATE_FOLDER", ""),
        *args, **kwargs
    )

    app.config.update(
        SERVER_NAME=os.getenv("SERVER_NAME", ""),
        SECRET_KEY=os.getenv("SECRET_KEY", str(secrets.token_hex())),
        PREFERRED_URL_SCHEME="https",
        CONTENT_FOLDER=os.getenv("CONTENT_FOLDER", ""),
        PRERENDER_CONTENT_FOLDER=os.getenv("PRERENDER_CONTENT_FOLDER", "")
    )

    app.register_blueprint(routes)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
