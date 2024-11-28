# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'DevOps 工程'
copyright = '2024, dengyouf'
author = 'dengyouf'
release = 'v0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['recommonmark','sphinx_markdown_tables']

templates_path = ['_templates']
exclude_patterns = []

language = 'zh-CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
# html_theme = "sphinxdoc"

# html_theme_options = {
#     "rightsidebar": "true",
#     "relbarbgcolor": "black"
# }
# html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_search_language = 'zh'
