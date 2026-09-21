"""
Pipeline entry point.

Run with:  python main.py
Runs Extract -> Transform -> Load in sequence and reports the outcome
of each stage.
"""

import sys
import os

from extract import extract
from transform import transform
from load import load

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "etl"))




def run_pipeline():
    print("=== EXTRACT ===")
    raw_df = extract()

    print("\n=== TRANSFORM ===")
    clean_df = transform(raw_df)

    print("\n=== LOAD ===")
    load(clean_df)
    
    print("\nPipeline complete.")


if __name__ == "__main__":
    run_pipeline()