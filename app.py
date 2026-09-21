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

# --- Design tokens -----------------------------------------------------------
NAVY = "#1B2A4A"
BG = "#F7F6F3"
SIDEBAR_BG = "#EDEAE2"
OCHRE = "#C98A3B"
GREEN = "#3F7860"
RUST = "#B4483A"
MUTED = "#6B6459"
CARD_BG = "#FFFFFF"

st.set_page_config(
    page_title="Graduate Employment Analytics",
    page_icon="🎓",
    layout="wide",
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'IBM Plex Sans', sans-serif;
}}

h1 {{
    font-family: 'Fraunces', serif !important;
    font-weight: 600 !important;
    color: {NAVY} !important;
}}

h2, h3 {{
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600 !important;
    color: {NAVY} !important;
}}

[data-testid="stSidebar"] {{
    background-color: {SIDEBAR_BG};
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 1.75rem;
    border-bottom: 1px solid #D9D4C7;
}}
.stTabs [data-baseweb="tab"] {{
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 500;
    color: {MUTED};
}}
.stTabs [aria-selected="true"] {{
    color: {NAVY} !important;
}}

hr {{
    border: none;
    border-top: 2px solid {OCHRE};
    margin: 0.25rem 0 1.5rem 0;
    width: 64px;
}}

.metric-card {{
    background: {CARD_BG};
    border-left: 4px solid {OCHRE};
    border-radius: 4px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.5rem;
}}
.metric-label {{
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.8rem;
    color: {MUTED};
    letter-spacing: 0.01em;
    margin-bottom: 0.15rem;
}}
.metric-value {{
    font-family: 'Fraunces', serif;
    font-size: 2.1rem;
    font-weight: 600;
    color: {NAVY};
    line-height: 1.15;
}}
</style>
""", unsafe_allow_html=True)


def metric_card(label: str, value: str, accent: str = OCHRE) -> str:
    return f"""
    <div class="metric-card" style="border-left-color:{accent};">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """


def style_chart(fig):
    fig.update_layout(
        font=dict(family="IBM Plex Sans, sans-serif", color=NAVY),
        plot_bgcolor=BG,
        paper_bgcolor=BG,
        margin=dict(l=10, r=10, t=30, b=10),
    )
    fig.update_xaxes(gridcolor="#E4E0D4")
    fig.update_yaxes(gridcolor="#E4E0D4")
    return fig


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

    # SQLite has no native boolean type, so this column round-trips as
    # 0/1 integers rather than True/False. Cast it back explicitly —
    # boolean masking (filtered[filtered["employed"]]) silently breaks
    # otherwise, since pandas treats an int Series as column labels,
    # not a mask.
    df["employed"] = df["employed"].astype(bool)

    return df


df = load_data()

# --- Header ------------------------------------------------------------------
st.title("Graduate Employment Analytics")
st.markdown(
    f"<span style='color:{MUTED};font-size:0.95rem;'>"
    "ETL pipeline output — graduate survey data, cleaned and loaded into SQLite"
    "</span>",
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)

# --- Sidebar -------------------------------------------------------------------
st.sidebar.markdown(f"<h3 style='color:{NAVY};'>Filters</h3>", unsafe_allow_html=True)
degrees = st.sidebar.multiselect("Degree", options=sorted(df["degree"].unique()))
years = st.sidebar.multiselect("Graduation year", options=sorted(df["graduation_year"].unique()))
status = st.sidebar.selectbox("Employment status", options=["All", "Employed", "Unemployed"])

filtered = df.copy()
if degrees:
    filtered = filtered[filtered["degree"].isin(degrees)]
if years:
    filtered = filtered[filtered["graduation_year"].isin(years)]
if status != "All":
    filtered = filtered[filtered["employment_status"] == status]

st.sidebar.markdown("---")
st.sidebar.caption(
    "Data engineering pipeline: extract → transform → load → this dashboard. "
    "See the README for the full architecture."
)

if filtered.empty:
    st.warning("No records match the current filters.")
    st.stop()

# --- Shared metrics ------------------------------------------------------------
total = len(filtered)
employed = int(filtered["employed"].sum())
rate = (employed / total * 100) if total else 0
avg_months = filtered.loc[filtered["employed"], "months_to_employment"].mean()

# --- Tabs ------------------------------------------------------------------
tab_overview, tab_degrees, tab_companies, tab_data = st.tabs(
    ["Overview", "Degrees & Skills", "Companies & Salary", "Explore Data"]
)

with tab_overview:
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(metric_card("Graduates", f"{total:,}", OCHRE), unsafe_allow_html=True)
    c2.markdown(metric_card("Employed", f"{employed:,}", GREEN), unsafe_allow_html=True)
    c3.markdown(metric_card("Employment Rate", f"{rate:.1f}%", OCHRE), unsafe_allow_html=True)
    c4.markdown(
        metric_card("Avg. Months to Employment", f"{avg_months:.1f}" if pd.notna(avg_months) else "—", MUTED),
        unsafe_allow_html=True,
    )

    st.write("")
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Employment Outcomes by Graduation Year")
        by_year = (
            filtered.groupby("graduation_year")["employed"]
            .mean().mul(100).reset_index(name="employment_rate")
        )
        fig = px.line(
            by_year, x="graduation_year", y="employment_rate", markers=True,
            labels={"employment_rate": "Employment Rate (%)", "graduation_year": "Graduation Year"},
        )
        fig.update_traces(line_color=OCHRE, marker_color=OCHRE, line_width=3)
        st.plotly_chart(style_chart(fig), width='stretch')

    with col2:
        st.subheader("Employment Status")
        status_counts = filtered["employment_status"].value_counts().reset_index()
        status_counts.columns = ["status", "count"]
        fig2 = px.pie(
            status_counts, names="status", values="count", hole=0.55,
            color="status", color_discrete_map={"Employed": GREEN, "Unemployed": RUST},
        )
        fig2.update_traces(textinfo="percent+label")
        st.plotly_chart(style_chart(fig2), width='stretch')

with tab_degrees:
    st.subheader("Employment Rate by Degree")
    by_degree = (
        filtered.groupby("degree")["employed"]
        .mean().mul(100).sort_values(ascending=False).reset_index(name="employment_rate")
    )
    fig3 = px.bar(
        by_degree, x="degree", y="employment_rate",
        labels={"employment_rate": "Employment Rate (%)", "degree": ""},
    )
    fig3.update_traces(marker_color=OCHRE)
    fig3.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(style_chart(fig3), width='stretch')

    st.subheader("Top Skills Among Employed Graduates")
    top_skills = (
        filtered[filtered["employed"]]["skill"]
        .value_counts().head(10).sort_values().reset_index()
    )
    top_skills.columns = ["skill", "count"]
    fig4 = px.bar(
        top_skills, x="count", y="skill", orientation="h",
        labels={"count": "Employed Graduates", "skill": ""},
    )
    fig4.update_traces(marker_color=GREEN)
    st.plotly_chart(style_chart(fig4), width='stretch')

with tab_companies:
    st.subheader("Top Hiring Companies")
    top_companies = (
        filtered[filtered["employed"]]["company"]
        .value_counts().head(10).sort_values().reset_index()
    )
    top_companies.columns = ["company", "graduates_hired"]
    fig5 = px.bar(
        top_companies, x="graduates_hired", y="company", orientation="h",
        labels={"graduates_hired": "Graduates Hired", "company": ""},
    )
    fig5.update_traces(marker_color=OCHRE)
    st.plotly_chart(style_chart(fig5), width='stretch')

    st.subheader("Salary Distribution by Degree")
    salaried = filtered[(filtered["employed"]) & (filtered["salary"] > 0)]
    if salaried.empty:
        st.info("No salaried, employed graduates in the current filter selection.")
    else:
        order = salaried.groupby("degree")["salary"].median().sort_values(ascending=False).index
        fig6 = px.box(
            salaried, x="degree", y="salary", category_orders={"degree": list(order)},
            labels={"salary": "Salary", "degree": ""},
        )
        fig6.update_traces(marker_color=GREEN, line_color=NAVY)
        fig6.update_layout(xaxis_tickangle=-30)
        st.plotly_chart(style_chart(fig6), width='stretch')

with tab_data:
    st.subheader(f"Filtered Records ({total:,})")
    st.dataframe(filtered, width='stretch', hide_index=True)
    
