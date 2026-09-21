# Graduate Employment Analytics Platform

A small data engineering project that turns messy graduate employment survey
data into a clean, queryable dataset — and a dashboard you can actually
explore it with.

## What does this do?

It takes a raw CSV of graduate survey responses (name, degree, employment
status, salary, etc.), cleans it up, loads it into a database, and serves it
through an interactive dashboard where you can filter by degree or
graduation year and see employment trends.

In short: **messy CSV → clean database → interactive dashboard.**

## Why was this built?

Graduate employment data is usually messy in predictable ways — duplicate
records, missing salary values for people who aren't employed yet,
inconsistent formatting. Rather than analysing that in a spreadsheet by
hand, this project builds a repeatable pipeline: run one command, and the
data is extracted, cleaned, validated, and loaded fresh every time.

It also exists as a portfolio project to demonstrate core data engineering
skills — ETL pipeline design, data cleaning/validation, relational data
modelling, and building a usable interface on top of a database — as a
step toward the cloud engineering and data engineering work I want to do.

## How does it work?

The pipeline has three stages, run in order by `main.py`:

1. **Extract** (`etl/extract.py`) — reads the raw survey data from
   `data/graduate_survey.csv` into a pandas DataFrame.
2. **Transform** (`etl/transform.py`) — cleans it: removes duplicates,
   fixes data types, standardises text fields, fills in missing values
   for unemployed graduates (they legitimately have no salary/company),
   drops invalid rows (e.g. impossible ages), and adds a couple of derived
   fields like `employment_status`.
3. **Load** (`etl/load.py`) — writes the cleaned data into a local SQLite
   database (`data/graduate_employment.db`), rebuilding the table each run
   so re-running the pipeline never creates duplicates.

Then `app.py` is a Streamlit dashboard that reads from that SQLite database
and displays employment rate, time-to-employment, and hiring trends, with
filters by degree and graduation year.

```text
graduate_survey.csv → extract() → transform() → load() → SQLite → Streamlit dashboard
```

## Getting started

```bash
pip install -r requirements.txt

python3 main.py          # runs the full ETL pipeline
streamlit run app.py     # launches the dashboard
```

## Project structure

```text
├── data/
│   ├── generate_data.py       # generates the synthetic survey dataset
│   ├── graduate_survey.csv    # raw input data
│   └── graduate_employment.db # SQLite output (created by the pipeline)
├── etl/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── app.py                     # Streamlit dashboard
├── main.py                    # pipeline entry point
└── requirements.txt
```

## Current status

**What's built and working:**
- Full ETL pipeline (extract → transform → load), idempotent on re-run
- SQLite as the storage layer
- Interactive Streamlit dashboard with filtering and charts
- The dataset is synthetic (generated with Faker), modelled on the kind
  of fields a real StatsSA graduate survey would have — not real StatsSA
  data

**Not yet built:**
- Automated tests (no test suite exists yet — this is the next priority)
- A REST API layer
- PostgreSQL (currently SQLite; would be the production choice)
- Docker / CI/CD
- Cloud deployment (AWS)

## Roadmap

These are intentionally *not* built yet, listed here as direction rather
than implemented features:

- Add a `tests/` suite (unit tests for `transform.py` first, since that's
  where the data quality logic lives)
- Move storage from SQLite to PostgreSQL
- Wrap the pipeline output in a small REST API
- Containerise with Docker
- Deploy to AWS (S3 for raw data, RDS for PostgreSQL)

WTC-CBHZRGG5