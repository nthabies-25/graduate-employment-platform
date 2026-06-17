import pandas as pd
import os 

def extract():
    path = os.path.join("data", "graduate_survey")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found at {path}. Run generate_data.py first.")


    df = pd.read_csv(path)

    
    print(f"Extracted {len(df)} records from {path}")
    print(df.info())

    return df
if __name__ == "__main__":
    extract()