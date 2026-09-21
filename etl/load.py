import os
import sqlite3

import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "graduate_employment.db")

TABLE_NAME = "graduates"


def load(df: pd.DataFrame, db_path: str = DB_PATH) -> None:
    """
    Load the cleaned dataframe into a SQLite database.

    Uses a full replace-on-load strategy: each run rebuilds the table
    from the current cleaned dataset. This keeps the pipeline idempotent
    - re-running it never creates duplicate rows - which matters because
    a portfolio project's pipeline needs to be safely re-runnable, not just
    runnable once.
    """
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)

        # A couple of indexes so the dashboard's group-by queries stay fast
        # even if this dataset grows.
        conn.execute(
            f"CREATE INDEX IF NOT EXISTS idx_degree ON {TABLE_NAME}(degree)"
        )
        conn.execute(
            f"CREATE INDEX IF NOT EXISTS idx_status ON {TABLE_NAME}(employment_status)"
        )
        conn.commit()

        count = conn.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
        print(f"Loaded {count} records into {db_path} (table: {TABLE_NAME})")
    finally:
        conn.close()


if __name__ == "__main__":
    from extract import extract
    from transform import transform

    raw_df = extract()
    clean_df = transform(raw_df)
    load(clean_df)
