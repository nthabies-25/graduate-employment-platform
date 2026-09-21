import os
import sqlite3
import tempfile
import unittest

import pandas as pd

from load import load


def make_clean_df():
    """A small dataframe shaped like transform()'s output."""
    return pd.DataFrame({
        "graduate_id": [1, 2],
        "name": ["Alice", "Bob"],
        "age": [22, 25],
        "gender": ["Female", "Male"],
        "degree": ["Computer Science", "Law"],
        "graduation_year": [2023, 2022],
        "employed": [True, False],
        "company": ["Acme", "Not Employed"],
        "salary": [30000.0, 0.0],
        "months_to_employment": [3.0, 0.0],
        "skill": ["Python", "SQL"],
        "employment_status": ["Employed", "Unemployed"],
        "years_since_graduation": [2, 3],
    })


class LoadTest(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmp_dir.name, "test.db")

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_load_creates_table_with_correct_row_count(self):
        df = make_clean_df()

        load(df, db_path=self.db_path)

        conn = sqlite3.connect(self.db_path)
        count = conn.execute("SELECT COUNT(*) FROM graduates").fetchone()[0]
        conn.close()

        self.assertEqual(count, 2)

    def test_load_is_idempotent_on_repeated_runs(self):
        df = make_clean_df()

        load(df, db_path=self.db_path)
        load(df, db_path=self.db_path)  # run twice, same data

        conn = sqlite3.connect(self.db_path)
        count = conn.execute("SELECT COUNT(*) FROM graduates").fetchone()[0]
        conn.close()

        self.assertEqual(count, 2)  # not 4 — the table is replaced, not appended to


if __name__ == "__main__":
    unittest.main()
