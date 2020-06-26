# Copyright © 2020 Clément Pit-Claudel
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from . import docutils
from .html import ASSETS

# Export here so config files can refer to just this module
RSTCoqParser = docutils.RSTCoqParser

# Setup
# =====

def register_coq_parser(app):
    app.add_source_parser(RSTCoqParser)
    app.add_source_suffix('.v', 'coq')

def add_html_assets(app):
    if app.builder.name == "html":
        app.config.html_static_path.append(ASSETS.PATH)

        for css in ASSETS.ALECTRYON_CSS + ASSETS.PYGMENTS_CSS:
            app.add_stylesheet(css)
        for js in ASSETS.ALECTRYON_JS:
            app.add_javascript(js)

def setup(app):
    """Register Alectryon's directives, transforms, etc."""

    for role in docutils.ROLES:
        app.add_role(role.name, role)

    for node in docutils.NODES:
        visit, depart = getattr(node, 'visit'), getattr(node, 'depart')
        if visit and depart:
            app.add_node(node,
                         html=(visit, depart),
                         latex=(visit, depart),
                         text=(visit, depart))

    for directive in docutils.DIRECTIVES:
        getattr(directive, "setup", lambda _: None)(app.srcdir)
        app.add_directive(directive.name, directive)

    for transform in docutils.TRANSFORMS:
        app.add_transform(transform)

    app.connect('builder-inited', add_html_assets)
    app.connect('builder-inited', register_coq_parser)

    return {'version': '0.1', "parallel_read_safe": True}