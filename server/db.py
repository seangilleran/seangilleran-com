""" db.py
"""

from pathlib import Path

from flask import current_app as app
from markdown import Markdown
from werkzeug.utils import secure_filename

# Try the faster LibYAML loader first, then fall back on the Python version.
# https://pyyaml.org/wiki/PyYAMLDocumentation
import yaml
try:
    from yaml import CLoader as YAMLLoader
except ImportError:
    from yaml import Loader as YAMLLoader


# See list of markdown extensions here:
# https://python-markdown.github.io/extensions/
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


def _get_html(name):

    # HTML content is rendered with Pandoc whenever we start the server. This
    # has two big advantages: first, it's faster than chunking through the
    # Markdown every single time we need to load the page. Second, it lets us
    # use otherwise troublesome features like citeproc without having to set up
    # a supplementary toolchain. The end result, ideally, should be one in
    # which blog posts can be rendered as PDFs and vice-versa using the exact
    # same Markdown and bibliographic JSON files.
    #
    # N.b.: rather than pull the metadata into the HTML files, (which Pandoc
    # doesn't want to do anyway without some coaxing) we can just render it
    # separately and load it as YAML data.

    filepath = Path(app.config["PRERENDER_CONTENT_FOLDER"])
    filepath, metapath = filepath / f"{name}.html", metapath / f"{name}.yaml"
    if not filepath.exists() or not metapath.exists():
        return None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read().strip()
        with open(metapath, "r", encoding="utf-8") as f:
            meta = yaml.load(f, loader=YAMLLoader)
    except Exception:
        return None

    if "description" not in meta:
        meta["description"] = html.splitlines()[0][3:-4]

    return html, meta


def _get_markdown(name):

    filepath = Path(app.config["CONTENT_FOLDER"]) / f"{name}.md"
    if not filepath.exists():
        return None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception:
        return None

    md = Markdown(extensions=_MD_PLUGINS)
    html = md.convert(text)
    meta = md.Meta
    if "description" not in meta:
        meta["description"] = html.splitlines()[0][3:-4]

    return html, meta


def get_post(name):

    # Make sure file system is not inadvertently being exposed to the web.
    # https://werkzeug.palletsprojects.com/en/2.0.x/utils/#werkzeug.utils.secure_filename
    name = secure_filename(name)

    data = _get_html(name)
    if not data:
        data = _get_markdown(name)
    return data


def get_page(name):

    # Pages use "_" as a prefix to distinguish them from blog posts.
    # This should be done via subdirectories in a later refactor.
    name = f"_{secure_filename(name)}"

    data = _get_html(name)
    if not data:
        data = _get_markdown(name)
    return data
