"""Student performance dashboard built around clear, reviewable analysis.

Run locally with: streamlit run app.py
All student and assessment records are synthetic.
"""
from pathlib import Path
import subprocess
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

st.set_page_config(page_title="Student Performance | Analytics", page_icon="🎓", layout="wide")

@st.cache_data
def load_data():
    student_path, assessment_path = DATA_DIR / "students.csv", DATA_DIR / "assessments.csv"
    if not student_path.exists() or not assessment_path.exists():
        subprocess.run([sys.executable, str(ROOT / "src" / "generate_data.py")], check=True)
    students = pd.read_csv(student_path)
    assessments = pd.read_csv(assessment_path)
    return students, assessments

students, assessments = load_data()
data = assessments.merge(students, on="student_id", how="left")
data["result"] = data["score"].ge(40).map({True: "Pass", False: "Below 40"})
data["term_label"] = "Term " + data["term"].astype(str)

st.title("Student Performance Dashboard")
st.caption("Explore attainment, subject trends and attendance patterns · Fictional portfolio dataset")

with st.sidebar:
    st.header("Report filters")
    cohorts = sorted(data["cohort"].dropna().unique())
    selected_cohorts = st.multiselect("Cohort", cohorts, default=cohorts)
    grades = sorted(data["grade"].dropna().unique().tolist())
    selected_grades = st.multiselect("Grade", grades, default=grades)
    subjects = sorted(data["subject"].dropna().unique())
    selected_subjects = st.multiselect("Subject", subjects, default=subjects)
    terms = sorted(data["term"].dropna().unique().tolist())
    selected_terms = st.multiselect("Term", terms, default=terms)

filtered = data[
    data["cohort"].isin(selected_cohorts)
    & data["grade"].isin(selected_grades)
    & data["subject"].isin(selected_subjects)
    & data["term"].isin(selected_terms)
].copy()

if filtered.empty:
    st.warning("No assessment records match these filters. Select at least one cohort, grade, subject and term.")
    st.stop()

average_score = filtered["score"].mean()
pass_rate = filtered["score"].ge(40).mean() * 100
average_attendance = filtered.drop_duplicates("student_id")["attendance_pct"].mean()
students_in_scope = filtered["student_id"].nunique()
below_threshold = filtered.loc[filtered["score"] < 40, "student_id"].nunique()

kpis = st.columns(5)
kpis[0].metric("Students", f"{students_in_scope:,}")
kpis[1].metric("Average score", f"{average_score:.1f}/100")
kpis[2].metric("Scores ≥ 40", f"{pass_rate:.1f}%")
kpis[3].metric("Average attendance", f"{average_attendance:.1f}%")
kpis[4].metric("Students below threshold", f"{below_threshold:,}")

left, right = st.columns(2)
with left:
    subject_summary = filtered.groupby("subject", as_index=False).agg(average_score=("score", "mean")).sort_values("average_score", ascending=True)
    fig = px.bar(subject_summary, x="average_score", y="subject", orientation="h", color="average_score", color_continuous_scale="Teal", title="Average score by subject", labels={"average_score": "Average score", "subject": ""})
    fig.add_vline(x=40, line_dash="dash", annotation_text="40-point reference")
    st.plotly_chart(fig, use_container_width=True)
with right:
    term_summary = filtered.groupby(["term", "term_label"], as_index=False).agg(average_score=("score", "mean")).sort_values("term")
    fig = px.line(term_summary, x="term_label", y="average_score", markers=True, title="Average score across terms", labels={"term_label": "Assessment term", "average_score": "Average score"})
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    fig = px.histogram(filtered, x="score", color="result", nbins=20, barmode="overlay", opacity=0.8, title="Score distribution", labels={"score": "Assessment score", "count": "Assessment records"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    attendance = filtered.drop_duplicates("student_id")
    fig = px.scatter(attendance, x="attendance_pct", y=attendance["student_id"].map(filtered.groupby("student_id")["score"].mean()), color="grade", hover_data=["student_id", "cohort"], title="Attendance and average score", labels={"attendance_pct": "Attendance (%)", "y": "Average score", "grade": "Grade"})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Student-level summary")
student_summary = filtered.groupby(["student_id", "grade", "cohort"], as_index=False).agg(average_score=("score", "mean"), attendance_pct=("attendance_pct", "first"), assessments=("assessment_id", "count"))
student_summary["review_flag"] = (student_summary["average_score"] < 40) | (student_summary["attendance_pct"] < 75)
st.caption("Review flag is a simple configurable screening rule for human follow-up, not a diagnosis or automated decision.")
st.dataframe(student_summary.sort_values(["review_flag", "average_score"], ascending=[False, True]), use_container_width=True, hide_index=True)
st.download_button("Download filtered student summary", student_summary.to_csv(index=False).encode("utf-8"), "student_performance_summary.csv", "text/csv")

with st.expander("Definitions and responsible use"):
    st.write("The pass reference is 40/100 for this demonstration only. The review flag marks records for a human to inspect; it must not be used to label, rank or make decisions about a student. All records are fictional.")
