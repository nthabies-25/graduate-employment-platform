"""
Graduate Employment Analytics Dashboard.

Run with: streamlit run app.py

Reads from the SQLite database produced by the ETL pipeline
(run `python main.py` first if data/graduate_employment.db doesn't exist yet).
"""
import os
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "graduate_employment.db")

st.set_page_config(page_title="Graduate Employment Analytics", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    if not os.path.exists(DB_PATH):
        st.error(
            "No database found. Run `python main.py` first to build the pipeline "
            "and populate data/graduate_employment.db."
        )
        st.stop()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM graduates", conn)
    conn.close()
    return df


df = load_data()

st.title("🎓 Graduate Employment Analytics")
st.caption("ETL pipeline output — extracted, cleaned, and loaded into SQLite")