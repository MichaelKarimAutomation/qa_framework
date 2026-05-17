"""Sphinx configuration for the qa-framework documentation build.

scripts/generate_docs.py orchestrates the full pipeline (clean previous
output, run sphinx-apidoc per package to emit per-module .rst files, then
sphinx-build to render HTML). This file only configures the rendering step.
"""
import sys
from pathlib import Path

# Make the repository root importable so autodoc can resolve `pom.*`,
# `utils.*`, etc., just like pytest does via `pythonpath = ["."]`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


project = 'qa-framework'
author = 'mkarim'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',       # pull docstrings out of imported modules
    'sphinx.ext.napoleon',      # accept Google / NumPy style docstrings
    'sphinx.ext.viewcode',      # add "[source]" links to each rendered symbol
]

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

# Mock Locust during autodoc import. Locust monkey-patches gevent/ssl at
# import time, which collides with httpx/urllib3 already loaded in the same
# process and triggers RecursionError. Mocking lets us still render the
# performance/ Locust files without actually importing the real package.
autodoc_mock_imports = ['locust']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
