import pandas as pd 

def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardise the raw graduate dataset, then derive
    analytics-ready fields.
    """
    df =df.copy()
    
    #Remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset="graduate_id")
    removed = before - len(df)
    if removed:
        print(f"Removed {removed} duplicate record(s)")
        
        #Standardize types
    df["employed"] = df["employed"].astype(bool)
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["graduation_year"] = pd.to_numeric(df["graduation_year"], errors="coerce")
    df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
    df["months_to_employment"] = pd.to_numeric(df["months_to_employment"], errors="coerce")
    
    #Standardize text fields(whitespaces)
    for col in ["name", "gender", "degree", "company", "skill"]:
        df[col] = df[col].astype("string").str.strip()
        
        