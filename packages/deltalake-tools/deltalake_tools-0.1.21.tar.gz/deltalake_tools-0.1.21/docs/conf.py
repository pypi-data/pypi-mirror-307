# docs/conf.py

import os
import sys
import tomllib  # or import tomllib if using Python 3.11+

# -- Path setup --------------------------------------------------------------

# Add the project's root directory to sys.path
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

# Read project metadata from pyproject.toml
with open("../pyproject.toml", "rb") as f:
    pyproject_data = tomllib.load(f)

project_info = pyproject_data.get("project", {})

project = project_info.get("name", "Your Project Name")
author = ", ".join([author["name"] for author in project_info.get("authors", [{"name": "Your Name"}])])
release = project_info.get("version", "0.1")
copyright = '2024, jeroenflvr'
# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']

exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']

# -- Extension configuration -------------------------------------------------

# Autodoc settings
autodoc_member_order = 'bysource'

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# Todo extension settings
todo_include_todos = True
