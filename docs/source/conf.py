# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'CyberArena'
copyright = '2022, Yasser OMARI, Alphée GROSDIDIER, Fantin GAUTHIER'
author = 'Yasser OMARI, Alphée GROSDIDIER, Fantin GAUTHIER'
release = 'pre-alpha'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = [
    'sphinx_rtd_theme',
    'sphinxcontrib.mermaid'
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_title = 'CyberArena'
html_logo = None
html_favicon = None
