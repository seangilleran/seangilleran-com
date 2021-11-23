""" db.py
"""

from pathlib import Path
import re

from flask import current_app as app
from markdown import Markdown
import yaml
try:
    from yaml import CLoader as YAMLLoader
except ImportError:
    from yaml import Loader as YAMLLoader


_RE_BAD_PATH = re.compile(r"[\\\/\.\*]")
_MD_PLUGINS = [
    "full_yaml_metadata",
    "smarty",
    "mdx_emdash",
    "pymdownx.saneheaders",
    "pymdownx.caret",
    "pymdownx.tilde",
    "pymdownx.mark",
    "pymdownx.smartsymbols",
    "pymdownx.emoji",
    "pymdownx.magiclink",
    "pymdownx.extra",
    "mdx_truly_sane_lists",
]


def _get_markdown(name):

    # Check file path for special characters--make sure we're not going outside the content path.
    filepath = Path(app.config["CONTENT_FOLDER"])
    filepath = filepath / f"{re.sub(_RE_BAD_PATH, '', name)}.md"
    if not filepath.exists():
        return None

    # Read content from file.
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception:
        return None

    md = Markdown(extensions=_MD_PLUGINS)
    html = md.convert(text)
    meta = md.Meta
    if "blurb" not in meta:
        meta["blurb"] = html.splitlines()[0][3:-4]

    html = "<!-- md -->\n" + html
    return html, meta


def _get_html(name):

    # Check file path for special characters--make sure we're not going outside the content path.
    filepath = Path(app.config["CONTENT_FOLDER"]) / ".html"
    name = f"{re.sub(_RE_BAD_PATH, '', name)}"
    filepath, metapath = filepath / f"{name}.html", filepath / f"{name}.yaml"
    if not filepath.exists() or not metapath.exists():
        return None

    # Read content from files.
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read().strip()
    except Exception:
        return None

    try:
        with open(metapath, "r", encoding="utf-8") as f:
            meta = yaml.load(f, loader=YAMLLoader)
    except Exception:
        return None
    if "blurb" not in meta:
        meta["blurb"] = html.splitlines()[0][3:-4]

    return html, meta


def get_page(name):
    data = _get_html(name)
    if not data:
        data = _get_markdown(name)
    return data
