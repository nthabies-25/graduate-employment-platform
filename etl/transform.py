import pandas as pd


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardise the raw graduate dataset, then derive
    analytics-ready fields.
    """
    df = df.copy()

    # --- Remove duplicates -------------------------------------------------
    before = len(df)
    df = df.drop_duplicates(subset="graduate_id")
    removed = before - len(df)
    if removed:
        print(f"Removed {removed} duplicate record(s)")

    # --- Standardise types ---------------------------------------------------
    df["employed"] = df["employed"].astype(bool)
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["graduation_year"] = pd.to_numeric(df["graduation_year"], errors="coerce")
    df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
    df["months_to_employment"] = pd.to_numeric(
        df["months_to_employment"], errors="coerce"
    )

    # --- Standardise text fields (whitespace/casing) --------------------------
    for col in ["name", "gender", "degree", "company", "skill"]:
        df[col] = df[col].astype("string").str.strip()

    # --- Handle missing values -------------------------------------------------
    # Unemployed graduates legitimately have no company/salary/time-to-employment.
    # Fill those explicitly rather than leaving ambiguous NaNs.
    df["company"] = df["company"].fillna("Not Employed")
    df["salary"] = df["salary"].fillna(0)
    df["months_to_employment"] = df["months_to_employment"].fillna(0)

    # --- Validate categorical values --------------------------------------------
    valid_genders = {"Male", "Female"}
    invalid_gender_mask = ~df["gender"].isin(valid_genders)
    if invalid_gender_mask.any():
        print(f"Dropping {invalid_gender_mask.sum()} record(s) with invalid gender")
        df = df[~invalid_gender_mask]

    # Drop rows with an impossible age or graduation year
    df = df[(df["age"] >= 18) & (df["age"] <= 65)]
    df = df[df["graduation_year"].between(2000, 2100)]

    # --- Derived fields ------------------------------------------------------
    df["employment_status"] = df["employed"].map({True: "Employed", False: "Unemployed"})

    current_year = pd.Timestamp.now().year
    df["years_since_graduation"] = current_year - df["graduation_year"]

    print(f"Transformed dataset: {len(df)} clean records")
    print(df["employment_status"].value_counts())

    return df


if __name__ == "__main__":
    from extract import extract

    raw_df = extract()
    clean_df = transform(raw_df)
    print(clean_df.head())
