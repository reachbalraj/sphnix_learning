# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
# sys.path.insert(0, os.path.abspath('.'))
import datetime
sys.path.append(os.path.abspath('utils'))
import json

project = 'sphnix_learning'
copyright = '2023, Balraj Ramalingam'
author = 'Balraj Ramalingam'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_needs',
    "sphinxcontrib.plantuml",
    "sphinx.ext.graphviz",

]


templates_path = ['_templates']
exclude_patterns = []


# -- Plantuml configuration --------------------------------------------------

# Plantuml headless mode, see https://sphinxcontrib-needs.readthedocs.io/en/latest/installation.html

plantuml = 'java -Djava.awt.headless=true -jar %s' % os.path.join(os.path.dirname(__file__), "utils", "plantuml", "plantuml.jar")

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- sphinx-needs configuration ----------------------------------------------

#need type definitions
needs_types = [dict(directive="ureq", title="Unit Requirement", prefix="UR_", color="#BFD8D2", style="node"),
               dict(directive="swreq", title="Software Requirement", prefix="SR_", color="#FEDCD2", style="node"),
               dict(directive="sysreq", title="System Requirement", prefix="SYSR_", color="#FEDCD2", style="node"),
               dict(directive="test", title="Test Case", prefix="T_", color="#DCB239", style="node")
              ]

# need option definitions
needs_extra_options = [
    "asil",
    "test_summary",
    "test_steps",
    "test_precondition",
    "test_expected_result",
    "test_verification_criteria",
    "rtc_status",
    "rtc_plannedfor",
    "soc_variant"
]

# need link definitions
needs_extra_links = [
   {
      "option": "depends",
      "incoming": "is depended by",
      "outgoing": "depends"
   },
   {
      "option": "implements",
      "incoming": "is implemented by",
      "outgoing": "implements"
   },
   {
      "option": "validates",
      "incoming": "is validated by",
      "outgoing": "validates"
   },
   {
      "option": "satisfies",
      "incoming": "is satisfied by",
      "outgoing": "satisfies"
   },
   {
      "option": "tests",
      "incoming": "is tested by",
      "outgoing": "tests"
   }
]

needs_warnings_always_warn = True

# Overwrite the default needs id regex expression since it only allows capital letters
# default: ^[A-Z0-9_]{5,}
needs_id_regex = "^[a-zA-Z0-9_]{5,}"

# Allows the creation of needs without titles
needs_title_optional = True

# Exports all needs into a JSON file
needs_build_json = True

# import color codes and define some roles
# :red:'some text'
# |br| for forced newline (break)
rst_prolog = """
.. include:: <s5defs.txt>
.. default-role:

.. |br| raw:: html

  <br/>
"""

warnings_filter_config = "warnings_filter_config.yml"
