import os
import sys

# Makes etl/extract.py, transform.py, load.py importable as plain modules
# (e.g. `from extract import extract`) when running the test suite,
# matching how the project's own scripts import each other.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "etl"))
