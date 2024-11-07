# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# import os
# sys.path.insert(0, os.path.abspath('../prism-python/'))

import os
import sys
import importlib
from datetime import datetime

sys.path.append("scripts")
sys.path.insert(0, os.path.abspath('../..'))
prismstudio = importlib.import_module("prismstudio") # used to resolve the import within the module, injecting it into the global namespace
prismstudio.login("demouser", "kqn&5bmXcMrPL6uxfyZ%s7")
globals()["prismstudio"] = prismstudio

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "PrismStudio"
copyright = f"{datetime.now().year}, Prism39"
author = "Prism39"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
    "numpydoc",
    "myst_parser",
    "sphinx_toggleprompt",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "sphinxext.rediraffe",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx_multiversion",
]


templates_path = ["_templates"]
exclude_patterns = []

numpydoc_attributes_as_param_list = False


myst_footnote_transition = False

toggleprompt_offset_right = 35

autodoc_typehints = "none"

panels_add_bootstrap_css = False

pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

autosummary_generate = True

html_logo = "_static/logo_light.svg"

html_theme = 'pydata_sphinx_theme'
html_favicon = "_static/favicon.ico"
html_static_path = ['_static', '_static/switcher.json']
html_css_files = ["prism_ov.css"]

source_suffix = [".rst", ".md"]

autodoc_default_options = {
    'undoc-members': False,
    'inherited-members': False,
    "show-inheritance": False,
}
inherited_members = False
# imported_members = False

ERROR_MSGS = {
    "GL01": "Docstring text (summary) should start in the line immediately "
}

version = ""

html_theme_options = {
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["versioning", "navbar-icon-links", "theme-switcher", "logout"], #"version-switcher",
    "navbar_persistent": ["search-button"],
    "navbar_align": "content", # [left, content, right]
    "primary_sidebar_end": [], # ["sidebar-ethical-ads"],
    "secondary_sidebar_items": [],
    'show_nav_level': 2,
    'navigation_depth': 4,
    "icon_links": [
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/prismstudio/",  # required
            "icon": "fa-solid fa-box",
        }
   ],
   "logo": {
        "image_dark": "_static/logo_dark.svg",
        "image_light": "_static/logo_light.svg",
        "alt_text": "PrismStudio Documentation",
    },
    "switcher": {
        "json_url": "_static/switcher.json",
        "version_match": version,
    },
}

# sphinx multiversion
smv_tag_whitelist = r'^(v\d+\.\d+\..+)|latest$'
smv_branch_whitelist = r'^None$'
smv_outputdir_format = 'versions/{ref.name}'

html_sidebars = {
    "index": [],  # Main Page
    "getstarted/*": ["prism_sidebar.html"],
    "userguide/*": ["prism_sidebar.html"],
    "releasenote/*": ["prism_sidebar.html"],
}

import sphinx  # isort:skip
from sphinx.ext.autodoc import (  # isort:skip
    AttributeDocumenter,
    Documenter,
    MethodDocumenter,
)
from sphinx.ext.autosummary import Autosummary  # isort:skip


class AccessorDocumenter(MethodDocumenter):
    """
    Specialized Documenter subclass for accessors.
    """

    objtype = "accessor"
    directivetype = "method"

    # lower than MethodDocumenter so this is not chosen for normal methods
    priority = 0.6

    def format_signature(self):
        # this method gives an error/warning for the accessors, therefore
        # overriding it (accessor has no arguments)
        return ""


class AccessorLevelDocumenter(Documenter):
    """
    Specialized Documenter subclass for objects on accessor level (methods,
    attributes).
    """

    # This is the simple straightforward version
    # modname is None, base the last elements (eg 'hour')
    # and path the part before (eg 'Series.dt')
    # def resolve_name(self, modname, parents, path, base):
    #     modname = 'pandas'
    #     mod_cls = path.rstrip('.')
    #     mod_cls = mod_cls.split('.')
    #
    #     return modname, mod_cls + [base]
    def resolve_name(self, modname, parents, path, base):
        if modname is None:
            if path:
                mod_cls = path.rstrip(".")
            else:
                mod_cls = None
                # if documenting a class-level object without path,
                # there must be a current class, either from a parent
                # auto directive ...
                mod_cls = self.env.temp_data.get("autodoc:class")
                # ... or from a class directive
                if mod_cls is None:
                    mod_cls = self.env.temp_data.get("py:class")
                # ... if still None, there's no way to know
                if mod_cls is None:
                    return None, []
            # HACK: this is added in comparison to ClassLevelDocumenter
            # mod_cls still exists of class.accessor, so an extra
            # rpartition is needed
            modname, _, accessor = mod_cls.rpartition(".")
            modname, _, cls = modname.rpartition(".")
            parents = [cls, accessor]
            # if the module name is still missing, get it like above
            if not modname:
                modname = self.env.temp_data.get("autodoc:module")
            if not modname:
                if sphinx.__version__ > "1.3":
                    modname = self.env.ref_context.get("py:module")
                else:
                    modname = self.env.temp_data.get("py:module")
            # ... else, it stays None, which means invalid
        return modname, parents + [base]


class AccessorAttributeDocumenter(AccessorLevelDocumenter, AttributeDocumenter):
    objtype = "accessorattribute"
    directivetype = "attribute"

    # lower than AttributeDocumenter so this is not chosen for normal
    # attributes
    priority = 0.6


class AccessorMethodDocumenter(AccessorLevelDocumenter, MethodDocumenter):
    objtype = "accessormethod"
    directivetype = "method"

    # lower than MethodDocumenter so this is not chosen for normal methods
    priority = 0.6


class AccessorCallableDocumenter(AccessorLevelDocumenter, MethodDocumenter):
    """
    This documenter lets us removes .__call__ from the method signature for
    callable accessors like Series.plot
    """

    objtype = "accessorcallable"
    directivetype = "method"

    # lower than MethodDocumenter; otherwise the doc build prints warnings
    priority = 0.5

    def format_name(self):
        if sys.version_info < (3, 9):
            # NOTE pyupgrade will remove this when we run it with --py39-plus
            # so don't remove the unnecessary `else` statement below
            from pandas.util._str_methods import removesuffix

            return removesuffix(MethodDocumenter.format_name(self), ".__call__")
        else:
            return MethodDocumenter.format_name(self).removesuffix(".__call__")


def process_class_docstrings(app, what, name, obj, options, lines):
    """
    For those classes for which we use ::

    :template: autosummary/class_without_autosummary.rst

    the documented attributes/methods have to be listed in the class
    docstring. However, if one of those lists is empty, we use 'None',
    which then generates warnings in sphinx / ugly html output.
    This "autodoc-process-docstring" event connector removes that part
    from the processed docstring.
    """
    if what == "class":
        joined = "\n".join(lines)

        templates = ['_templates']

        for template in templates:
            if template in joined:
                joined = joined.replace(template, "")

        lines[:] = joined.split("\n")


def rstjinja(app, docname, source):
    """
    Render our pages as a jinja template for fancy templating goodness.
    """
    # https://www.ericholscher.com/blog/2016/jul/25/integrating-jinja-rst-sphinx/
    # Make sure we're outputting HTML
    if app.builder.format != "html":
        return
    src = source[0]
    rendered = app.builder.templates.render_string(src, app.config.html_context)
    source[0] = rendered


def skip_member(app, what, name, obj, skip, opts):
    # we can document otherwise excluded entities here by returning False
    # or skip otherwise included entities by returning True
    # if opts:
    #     print("opts", opts)
    if what == "method" or what == "attribute":
        # if what == "method":
        #     print(obj, what)
        return True
    return False


language = "en"

def setup(app):
    app.connect("source-read", rstjinja)
    app.connect("autodoc-process-docstring", process_class_docstrings)
    app.connect("autodoc-skip-member", skip_member)
    app.add_autodocumenter(AccessorDocumenter)
    app.add_autodocumenter(AccessorAttributeDocumenter)
    app.add_autodocumenter(AccessorMethodDocumenter)
    app.add_autodocumenter(AccessorCallableDocumenter)