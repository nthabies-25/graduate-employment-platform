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

# --- Sidebar filters -------------------------------------------------------
st.sidebar.header("Filters")
degrees = st.sidebar.multiselect(
    "Degree", options=sorted(df["degree"].unique()), default=None
)
years = st.sidebar.multiselect(
    "Graduation year", options=sorted(df["graduation_year"].unique()), default=None
)

filtered = df.copy()
if degrees:
    filtered = filtered[filtered["degree"].isin(degrees)]
if years:
    filtered = filtered[filtered["graduation_year"].isin(years)]

# --- Top-line metrics --------------------------------------------------------
total = len(filtered)
employed = int(filtered["employed"].sum())
rate = (employed / total * 100) if total else 0
avg_months = filtered.loc[filtered["employed"], "months_to_employment"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Graduates", total)
col2.metric("Employed", employed)
col3.metric("Employment Rate", f"{rate:.1f}%")
col4.metric("Avg. Months to Employment", f"{avg_months:.1f}" if pd.notna(avg_months) else "—")

st.divider()

# --- Charts ----------------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Employment Rate by Degree")
    by_degree = (
        filtered.groupby("degree")["employed"]
        .mean()
        .mul(100)
        .sort_values(ascending=False)
        .reset_index(name="employment_rate")
    )
    fig = px.bar(by_degree, x="degree", y="employment_rate", labels={"employment_rate": "Employment Rate (%)"})
    fig.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Graduates by Employment Status")
    status_counts = filtered["employment_status"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]
    fig2 = px.pie(status_counts, names="status", values="count")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Employment Outcomes Over Graduation Years")
by_year = (
    filtered.groupby("graduation_year")["employed"]
    .mean()
    .mul(100)
    .reset_index(name="employment_rate")
)
fig3 = px.line(by_year, x="graduation_year", y="employment_rate", markers=True,
               labels={"employment_rate": "Employment Rate (%)"})
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Top Hiring Companies")
top_companies = (
    filtered[filtered["employed"]]["company"]
    .value_counts()
    .head(10)
    .reset_index()
)
top_companies.columns = ["company", "graduates_hired"]
st.dataframe(top_companies, use_container_width=True, hide_index=True)

with st.expander("View raw data"):
    st.dataframe(filtered, use_container_width=True)
