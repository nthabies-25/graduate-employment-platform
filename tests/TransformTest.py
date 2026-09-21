import unittest

import pandas as pd

from transform import transform


def make_df(**overrides):
    """Small, controllable dataset for testing transform() in isolation
    from the real CSV."""
    base = {
        "graduate_id": [1, 2, 3],
        "name": [" Alice ", "Bob", "Carol"],
        "age": [22, 25, 23],
        "gender": ["Female", "Male", "Female"],
        "degree": ["Computer Science", "Law", "Computer Science"],
        "graduation_year": [2023, 2022, 2024],
        "employed": [True, False, True],
        "company": ["Acme", None, "Globex"],
        "salary": [30000.0, None, 45000.0],
        "months_to_employment": [3.0, None, 5.0],
        "skill": ["Python", "SQL", "Java"],
    }
    base.update(overrides)
    return pd.DataFrame(base)


class TransformTest(unittest.TestCase):

    def test_removes_duplicate_graduate_ids(self):
        df = make_df()
        with_duplicate = pd.concat([df, df.iloc[[0]]], ignore_index=True)

        result = transform(with_duplicate)

        self.assertTrue(result["graduate_id"].is_unique)
        self.assertEqual(len(result), 3)

    def test_fills_missing_values_for_unemployed_graduates(self):
        df = make_df()

        result = transform(df)

        unemployed_row = result[result["employed"] == False].iloc[0]
        self.assertEqual(unemployed_row["company"], "Not Employed")
        self.assertEqual(unemployed_row["salary"], 0)
        self.assertEqual(unemployed_row["months_to_employment"], 0)

    def test_strips_whitespace_from_text_fields(self):
        df = make_df()

        result = transform(df)

        name = result.loc[result["graduate_id"] == 1, "name"].iloc[0]
        self.assertEqual(name, "Alice")

    def test_drops_rows_with_invalid_gender(self):
        df = make_df(gender=["Female", "Male", "Other"])

        result = transform(df)

        self.assertLessEqual(set(result["gender"].unique()), {"Male", "Female"})
        self.assertEqual(len(result), 2)

    def test_drops_rows_with_impossible_age(self):
        df = make_df(age=[22, 17, 90])

        result = transform(df)

        self.assertTrue(result["age"].between(18, 65).all())

    def test_creates_correct_employment_status(self):
        df = make_df()

        result = transform(df)

        self.assertLessEqual(set(result["employment_status"]), {"Employed", "Unemployed"})
        employed_row = result[result["employed"] == True].iloc[0]
        self.assertEqual(employed_row["employment_status"], "Employed")
        unemployed_row = result[result["employed"] == False].iloc[0]
        self.assertEqual(unemployed_row["employment_status"], "Unemployed")

    def test_years_since_graduation_is_non_negative(self):
        df = make_df()

        result = transform(df)

        self.assertTrue((result["years_since_graduation"] >= 0).all())


if __name__ == "__main__":
    unittest.main()
