from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

from talent_agent import (
    agent_answer as answer_talent_question,
    format_count,
    load_talent_data as load_talent_dataset,
    normalize_text as normalize,
)

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"

FRL_FILE = OUTPUT_DIR / "fRL_winners.xlsx"


@st.cache_data
def load_talent_data():
    return load_talent_dataset()


@st.cache_data
def load_frl_winners():
    if not FRL_FILE.exists():
        return pd.DataFrame()

    df = pd.read_excel(FRL_FILE)

    for col in ["Start Date", "End Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%d-%b-%Y")

    return df


def agent_answer(question, talent_df):
    return answer_talent_question(question, talent_df)


def set_demo_question(question, talent_df):
    st.session_state.question_text = question
    st.session_state.agent_response = agent_answer(question, talent_df)


def render_css():
    st.markdown("""
    <style>
    .block-container { padding-top: 1.35rem; max-width: 1240px; }
    .topbar {
        border: 1px solid #e5e7eb; border-radius: 10px; padding: 18px 20px;
        margin-bottom: 18px; background: #ffffff;
    }
    .topbar h1 { margin: 0 0 4px 0; font-size: 32px; color: #111827; }
    .topbar p { margin: 0; color: #4b5563; font-size: 15px; }
    .answer-box {
        background: #ffffff; color: #111827; border-left: 5px solid #2563eb;
        padding: 16px 18px; border-radius: 8px; border: 1px solid #e5e7eb;
        font-size: 16px; line-height: 1.6; font-weight: 500; margin-top: 14px;
    }
    .agent-note {
        background: #f8fafc; color: #111827; border: 1px solid #e5e7eb;
        padding: 14px 16px; border-radius: 8px; margin-top: 18px;
    }
    div[data-testid="stButton"] button { white-space: normal; text-align: left; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div class="topbar">
        <h1>foundit Talent Operations Assistant</h1>
        <p>IT/ITeS talent supply lookup and fRL winner automation</p>
    </div>
    """, unsafe_allow_html=True)


def render_agent_tab(talent_df):
    st.subheader("Talent Supply Agent")

    if "question_text" not in st.session_state:
        st.session_state.question_text = "How many AI/ML Engineer profiles are available in India?"
    if "agent_response" not in st.session_state:
        st.session_state.agent_response = ""

    left, right = st.columns([2, 1], gap="large")

    with left:
        question = st.text_input("Ask a Sales or Customer Success question", key="question_text")

        if st.button("Ask Agent", type="primary"):
            st.session_state.agent_response = agent_answer(question, talent_df)

        if st.session_state.agent_response:
            st.markdown(f"<div class='answer-box'>{st.session_state.agent_response}</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="agent-note">
        <b>Agent behavior:</b> The assistant answers from the supplied talent data.
        If the requested field is not available, it clearly says so instead of estimating.
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("#### Sample questions")
        demo_questions = [
            "How many AI/ML Engineer profiles are available in India?",
            "Which is larger - Data Scientist or DevOps talent, and by how much?",
            "How many 3-5y profiles are available?",
            "How many Pune profiles are available?",
            "What salary should I offer a DevOps engineer in Pune?",
        ]

        for i, demo_question in enumerate(demo_questions):
            st.button(
                demo_question,
                key=f"demo_{i}",
                on_click=set_demo_question,
                args=(demo_question, talent_df),
            )


def render_talent_dashboard(talent_df):
    st.subheader("Talent Supply Overview")

    def metric_value(label):
        row = talent_df[talent_df["Category Lower"] == normalize(label)]
        return format_count(row.iloc[0]["Profiles"]) if not row.empty else "NA"

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Profiles", metric_value("Total Profiles"))
    c2.metric("12M Active Profiles", metric_value("12M Active Profiles"))
    c3.metric("AI/ML Engineer", metric_value("AI/ML Engineer"))
    c4.metric("DevOps Engineer", metric_value("DevOps Engineer"))

    chart_df = talent_df[
        ~talent_df["Category Lower"].isin([
            "total profiles", "all time sourced", "all time registered",
            "by gender total profiles", "by experience total profiles",
            "location total profiles", "roles total profiles",
            "sub industry total profiles", "tier ii cities total profiles",
            "tier iii cities total profiles",
        ])
    ].head(24)

    fig = px.bar(
        chart_df,
        x="Profiles",
        y="Category",
        orientation="h",
        text="Profiles Display",
        title="Talent Categories Available In Source Data",
        color_discrete_sequence=["#2563eb"],
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        height=720,
        yaxis={"categoryorder": "total ascending"},
        margin=dict(l=20, r=40, t=60, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, width="stretch")

    with st.expander("View source knowledge base"):
        st.dataframe(talent_df[["Category", "Profiles", "Profiles Display"]], width="stretch", hide_index=True)


def render_frl_winners(frl_df):
    st.subheader("fRL Winners")

    if frl_df.empty:
        st.warning("fRL winners file not found. Run `python src/calculate_frl_winners.py` first.")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Winners", len(frl_df))
    c2.metric("Category Winners", len(frl_df[frl_df["Category"] != "MVP"]))
    c3.metric("MVP Winners", len(frl_df[frl_df["Category"] == "MVP"]))

    filter_col1, filter_col2, filter_col3 = st.columns(3)
    category_options = sorted(frl_df["Category"].dropna().astype(str).unique())
    user_type_options = sorted(frl_df["User Type"].dropna().astype(str).unique())
    service_options = sorted(frl_df["Service Channel"].dropna().astype(str).unique())

    selected_categories = filter_col1.multiselect(
        "Category",
        category_options,
        default=category_options,
    )
    selected_user_types = filter_col2.multiselect(
        "User Type",
        user_type_options,
        default=user_type_options,
    )
    selected_services = filter_col3.multiselect(
        "Service Channel",
        service_options,
        default=service_options,
    )

    filtered_df = frl_df[
        frl_df["Category"].astype(str).isin(selected_categories)
        & frl_df["User Type"].astype(str).isin(selected_user_types)
        & frl_df["Service Channel"].astype(str).isin(selected_services)
    ].copy()

    display_df = filtered_df.copy()
    display_df[["MVP Rank", "MVP Score"]] = display_df[
        ["MVP Rank", "MVP Score"]
    ].astype(str)
    st.dataframe(display_df, width="stretch", hide_index=True)

    if FRL_FILE.exists():
        with open(FRL_FILE, "rb") as file:
            st.download_button(
                label="Download winners Excel",
                data=file,
                file_name="fRL_winners.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

    chart_df = filtered_df.copy()
    if chart_df.empty:
        st.info("No winners match the selected filters.")
        return

    chart_df["MVP Score Numeric"] = pd.to_numeric(chart_df["MVP Score"], errors="coerce")
    chart_df["Display Score"] = chart_df["MVP Score Numeric"].fillna(
        chart_df[["PC", "OC", "JP"]].apply(pd.to_numeric, errors="coerce").max(axis=1)
    )

    fig = px.bar(
        chart_df,
        x="Display Score",
        y="Company Name",
        color="Category",
        orientation="h",
        title="Winner Score View",
    )
    fig.update_layout(height=650, yaxis={"categoryorder": "total ascending"}, plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, width="stretch")


def main():
    st.set_page_config(page_title="foundit Talent Operations Assistant", layout="wide")
    render_css()
    render_header()

    talent_df = load_talent_data()
    frl_df = load_frl_winners()

    tab1, tab2, tab3 = st.tabs(["Talent Agent", "Talent Dashboard", "fRL Winners"])

    with tab1:
        render_agent_tab(talent_df)
    with tab2:
        render_talent_dashboard(talent_df)
    with tab3:
        render_frl_winners(frl_df)


if __name__ == "__main__":
    main()
