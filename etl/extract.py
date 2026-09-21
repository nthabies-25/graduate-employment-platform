import pandas as pd
import os

# Project root = one level up from this file (etl/), so this works
# whether you run `python etl/extract.py` or `python extract.py` from etl/.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def extract():
    path = os.path.join(PROJECT_ROOT, "data", "graduate_survey.csv")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found at {path}. Run generate_data.py first.")


    df = pd.read_csv(path)

    
    print(f"Extracted {len(df)} records from {path}")
    print(df.info())

    return df
if __name__ == "__main__":
    extract()