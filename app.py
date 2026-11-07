"""Academic insight dashboard for fictional student performance data.

Run with: streamlit run app.py
"""
from pathlib import Path
import subprocess
import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
PASS_MARK = 40

st.set_page_config(page_title="LearnLens | Academic Insights", page_icon="✦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;600;700;800;900&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Nunito Sans',sans-serif;}
.stApp{background:#F8F7FC;color:#282343;}
[data-testid="stSidebar"]{background:#29234C;}
[data-testid="stSidebar"] *{color:#F4F0FF !important;}
[data-testid="stMetric"]{background:#FFFFFF;border:1px solid #E8E2F5;padding:18px;border-radius:18px;box-shadow:0 5px 18px rgba(60,44,110,.05);}
[data-testid="stMetricLabel"]{color:#81789B;}
[data-testid="stMetricValue"]{color:#352B69;font-family:'Plus Jakarta Sans',sans-serif;}
h1,h2,h3{font-family:'Plus Jakarta Sans',sans-serif;color:#352B69;}
.block-container{padding-top:2rem;max-width:1450px;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    student_file, assessment_file = DATA_DIR / "students.csv", DATA_DIR / "assessments.csv"
    if not student_file.exists() or not assessment_file.exists():
        subprocess.run([sys.executable, str(ROOT / "src" / "generate_data.py")], check=True)
    students = pd.read_csv(student_file)
    assessments = pd.read_csv(assessment_file)
    return assessments.merge(students, on="student_id", how="left")

data = load_data()
st.markdown("<div style='background:linear-gradient(115deg,#332A68,#6852A8);padding:25px 30px;border-radius:22px;color:white;margin-bottom:20px'><div style='font-size:12px;letter-spacing:2px;color:#F4C96B;font-weight:900'>LEARNLENS • ACADEMIC INTELLIGENCE</div><div style='font-family:Plus Jakarta Sans;font-size:32px;font-weight:800;color:white'>Learning Progress Studio</div><div style='color:#E6DFFB;margin-top:6px'>Understand achievement, subject strengths and where support may help</div></div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ✦ LEARNLENS")
    st.caption("STUDENT SUCCESS ANALYTICS")
    st.markdown("---")
    cohorts = sorted(data.cohort.dropna().unique())
    cohort_filter = st.multiselect("Academic cohort", cohorts, default=cohorts)
    grades = sorted(data.grade.dropna().unique().tolist())
    grade_filter = st.multiselect("Grade level", grades, default=grades)
    subjects = sorted(data.subject.dropna().unique())
    subject_filter = st.multiselect("Learning area", subjects, default=subjects)
    terms = sorted(data.term.dropna().unique().tolist())
    term_filter = st.multiselect("Assessment term", terms, default=terms)
    pass_mark = st.slider("Pass reference score", 0, 100, PASS_MARK)

view = data[data.cohort.isin(cohort_filter) & data.grade.isin(grade_filter) & data.subject.isin(subject_filter) & data.term.isin(term_filter)].copy()
if view.empty:
    st.warning("No assessment results match these selections.")
    st.stop()

student_level = view.groupby(["student_id","grade","cohort"], as_index=False).agg(Average_score=("score","mean"), Attendance=("attendance_pct","first"))
student_level["Support_review"] = (student_level.Average_score < pass_mark) | (student_level.Attendance < 75)
avg_score = view.score.mean()
pass_rate = view.score.ge(pass_mark).mean() * 100
avg_attendance = student_level.Attendance.mean()
student_count = view.student_id.nunique()
review_count = int(student_level.Support_review.sum())

kpi = st.columns(4)
kpi[0].metric("Learners in view", f"{student_count:,}")
kpi[1].metric("Average attainment", f"{avg_score:.1f} / 100")
kpi[2].metric("Meeting pass reference", f"{pass_rate:.1f}%")
kpi[3].metric("Average attendance", f"{avg_attendance:.1f}%")

st.markdown("### Learning outcomes")
left, right = st.columns([1.25, 1])
with left:
    heat = view.pivot_table(index="subject", columns="term", values="score", aggfunc="mean")
    fig = px.imshow(heat, text_auto=".1f", aspect="auto", color_continuous_scale=["#F4E9D1","#B7A4E7","#58469B"], labels={"x":"Term","y":"Subject","color":"Mean score"})
    fig.update_layout(title="Subject × term achievement map", paper_bgcolor="white", font_color="#352B69", margin=dict(l=10,r=10,t=55,b=10))
    st.plotly_chart(fig, use_container_width=True)
with right:
    fig = px.violin(view, x="subject", y="score", color="subject", box=True, points=False, color_discrete_sequence=["#6E5AA8","#E5B95C","#A18AD2","#79B9AE","#D58C9D"])
    fig.update_layout(title="Score spread by subject", showlegend=False, paper_bgcolor="white", plot_bgcolor="white", font_color="#352B69", xaxis_title="", yaxis_title="Assessment score", margin=dict(l=10,r=10,t=55,b=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("### Progress and learning habits")
left, right = st.columns(2)
with left:
    term_progress = view.groupby(["term"], as_index=False).agg(Mean_score=("score","mean"))
    fig = px.line(term_progress, x="term", y="Mean_score", markers=True, line_shape="spline", color_discrete_sequence=["#6954A5"])
    fig.update_traces(line=dict(width=4), marker=dict(size=10))
    fig.add_hline(y=pass_mark, line_dash="dot", line_color="#D59D37", annotation_text="Pass reference")
    fig.update_layout(title="Average attainment across terms", paper_bgcolor="white", plot_bgcolor="white", font_color="#352B69", xaxis_title="Term", yaxis_title="Average score", margin=dict(l=10,r=10,t=55,b=10))
    st.plotly_chart(fig, use_container_width=True)
with right:
    scatter = student_level.copy()
    fig = px.scatter(scatter, x="Attendance", y="Average_score", color="grade", size="Average_score", hover_data=["cohort"], color_continuous_scale="Purples", labels={"Attendance":"Attendance (%)","Average_score":"Average score","grade":"Grade"})
    fig.update_layout(title="Attendance and average achievement", paper_bgcolor="white", plot_bgcolor="white", font_color="#352B69", margin=dict(l=10,r=10,t=55,b=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("### Learner support overview")
flagged = student_level[student_level.Support_review]
support_share = len(flagged) / max(len(student_level), 1) * 100
st.markdown(f"<div style='background:#FFF8E8;border:1px solid #F2DFB6;padding:17px 20px;border-radius:14px'><span style='color:#805A16;font-weight:800;font-size:23px'>{review_count:,} learners</span><span style='color:#735E37'> ({support_share:.1f}% of learners in this view) meet the sample review rule.</span><br><span style='font-size:13px;color:#806F50'>Rule: average score below {pass_mark} or attendance below 75%. This is a prompt for supportive human review, not a prediction or student label.</span></div>", unsafe_allow_html=True)
student_level["Learner reference"] = student_level.student_id.map(lambda value: f"L-{value:04d}")
st.dataframe(student_level[["Learner reference","grade","cohort","Average_score","Attendance","Support_review"]].sort_values(["Support_review","Average_score"], ascending=[False,True]), use_container_width=True, hide_index=True)
st.download_button("Download learner summary", student_level.to_csv(index=False).encode("utf-8"), "learner_progress_summary.csv", "text/csv")

with st.expander("Definitions and responsible use"):
    st.write("All student records are fictional. The pass reference is configurable and set to 40 by default for this sample. Attendance and score patterns are descriptive, not proof of causation. The support rule must not be used to rank or make automated decisions about real students.")
st.caption("LEARNLENS • Academic insight from synthetic portfolio data")
