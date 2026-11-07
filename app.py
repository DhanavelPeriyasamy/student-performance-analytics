"""Student performance dashboard | Excel companion web view."""
from pathlib import Path
import subprocess
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data"
st.set_page_config(page_title="Student Performance | Dhanavel Periyasamy",page_icon="▦",layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:Inter,sans-serif;}
.stApp{background:#F7F7FA;color:#24243A;}
.block-container{max-width:1500px;padding-top:2rem;padding-bottom:3rem;}
[data-testid="stMetric"]{background:#FFFFFF;border:1px solid #E6E6EF;border-radius:12px;padding:17px 18px;box-shadow:0 2px 8px rgba(44,38,82,.035);}
[data-testid="stMetricLabel"]{color:#72728A;font-size:13px;}
[data-testid="stMetricValue"]{color:#37336F;font-weight:750;}
h1,h2,h3{color:#37336F;letter-spacing:-.025em;}
div[data-testid="stMultiSelect"] label,div[data-testid="stSlider"] label{font-weight:650;color:#62627A;}
div[data-testid="stPlotlyChart"]{background:#FFFFFF;border:1px solid #E8E8F0;border-radius:12px;padding:8px;}
hr{border-color:#E8E8F0;}
</style>
""",unsafe_allow_html=True)

@st.cache_data
def load_data():
    sf,af=DATA/"students.csv",DATA/"assessments.csv"
    if not sf.exists() or not af.exists():
        subprocess.run([sys.executable,str(ROOT/"src"/"generate_data.py")],check=True)
    students=pd.read_csv(sf)
    assessments=pd.read_csv(af)
    return assessments.merge(students,on="student_id",how="left")

df=load_data()
st.markdown("""
<div style="background:#302F63;border-radius:16px;padding:27px 30px;color:white;margin-bottom:20px">
<div style="font-size:11px;letter-spacing:2px;font-weight:700;color:#D5C8FF">EDUCATION ANALYTICS • LEARNING OUTCOMES</div>
<div style="font-size:31px;font-weight:800;letter-spacing:-1px;color:#FFFFFF;margin-top:5px">Student Performance Dashboard</div>
<div style="font-size:14px;color:#E4E1F5;margin-top:7px">Achievement, subject comparisons and attendance patterns across cohorts</div>
</div>
""",unsafe_allow_html=True)

st.markdown("**REPORT FILTERS**")
f1,f2,f3,f4,f5=st.columns([1.1,1,1.25,1,1])
cohorts=sorted(df.cohort.dropna().unique())
cohort_filter=f1.multiselect("Cohort",cohorts,default=cohorts,placeholder="All cohorts")
grades=sorted(df.grade.dropna().unique())
grade_filter=f2.multiselect("Grade",grades,default=grades,placeholder="All grades")
subjects=sorted(df.subject.dropna().unique())
subject_filter=f3.multiselect("Subject",subjects,default=subjects,placeholder="All subjects")
terms=sorted(df.term.dropna().unique())
term_filter=f4.multiselect("Term",terms,default=terms,placeholder="All terms")
pass_mark=f5.slider("Pass mark",0,100,40)
view=df[df.cohort.isin(cohort_filter)&df.grade.isin(grade_filter)&df.subject.isin(subject_filter)&df.term.isin(term_filter)].copy()
st.divider()
if view.empty:
    st.info("No assessment records match the selected filters. Expand your selections.")
    st.stop()

student_summary=view.groupby(["student_id","grade","cohort"],as_index=False).agg(Average_score=("score","mean"),Attendance=("attendance_pct","first"))
student_summary["Support_review"]=(student_summary.Average_score<pass_mark)|(student_summary.Attendance<75)
student_count=view.student_id.nunique()
average=view.score.mean()
pass_rate=view.score.ge(pass_mark).mean()*100
attendance=student_summary.Attendance.mean()
review_count=int(student_summary.Support_review.sum())

st.markdown("### Academic overview")
k=st.columns(5)
k[0].metric("Students",f"{student_count:,}")
k[1].metric("Assessments",f"{len(view):,}")
k[2].metric("Average score",f"{average:.1f}/100")
k[3].metric("At / above pass mark",f"{pass_rate:.1f}%")
k[4].metric("Average attendance",f"{attendance:.1f}%")
st.markdown("### Subject achievement")
left,right=st.columns([1.35,1])
with left:
    heat=view.pivot_table(index="subject",columns="term",values="score",aggfunc="mean")
    fig=px.imshow(heat,text_auto=".1f",aspect="auto",color_continuous_scale=["#F0EDFA","#A9A0D7","#514D91"],title="Average score by subject and term",labels={"x":"Term","y":"Subject","color":"Average score"})
    fig.update_layout(template="plotly_white",height=350,margin=dict(l=18,r=18,t=55,b=15),font_color="#45445F")
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
with right:
    subject_perf=view.groupby("subject",as_index=False).agg(Average_score=("score","mean")).sort_values("Average_score")
    fig=px.bar(subject_perf,x="Average_score",y="subject",orientation="h",text_auto=".1f",title="Subject average",color_discrete_sequence=["#625BA8"])
    fig.update_layout(template="plotly_white",height=350,margin=dict(l=18,r=18,t=55,b=15),xaxis_title="Average score",yaxis_title="",font_color="#45445F",xaxis_range=[0,100])
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
st.markdown("### Progress and learning habits")
left,right=st.columns(2)
with left:
    term_trend=view.groupby("term",as_index=False).agg(Average_score=("score","mean"))
    fig=px.line(term_trend,x="term",y="Average_score",markers=True,title="Average score across terms",color_discrete_sequence=["#625BA8"])
    fig.add_hline(y=pass_mark,line_dash="dash",line_color="#D49A45",annotation_text="Pass mark")
    fig.update_traces(line_width=3,marker_size=8)
    fig.update_layout(template="plotly_white",height=320,margin=dict(l=18,r=18,t=55,b=15),xaxis_title="Term",yaxis_title="Average score",font_color="#45445F",yaxis_range=[0,100])
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
with right:
    fig=px.scatter(student_summary,x="Attendance",y="Average_score",color="grade",title="Attendance and average score",labels={"Attendance":"Attendance (%)","Average_score":"Average score"},color_discrete_sequence=["#625BA8","#9A91C9","#D3A65C","#7B9F9A"])
    fig.add_hline(y=pass_mark,line_dash="dash",line_color="#D49A45")
    fig.update_layout(template="plotly_white",height=320,margin=dict(l=18,r=18,t=55,b=15),font_color="#45445F",xaxis_range=[0,100],yaxis_range=[0,100],legend_title="Grade")
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
st.markdown("### Learner support review")
share=review_count/max(len(student_summary),1)*100
st.markdown(f"<div style='background:#F0EFF8;border:1px solid #E1DFF0;border-radius:10px;padding:15px 18px;margin:8px 0 16px'><b style='color:#37336F'>{review_count:,} learners ({share:.1f}%)</b><span style='color:#66647D'> meet the sample review rule: average score below {pass_mark} or attendance below 75%. This is a prompt for supportive human review, not a prediction or student label.</span></div>",unsafe_allow_html=True)
student_summary["Learner reference"]=student_summary.student_id.map(lambda x:f"L-{x:04d}")
st.dataframe(student_summary[["Learner reference","grade","cohort","Average_score","Attendance","Support_review"]].sort_values(["Support_review","Average_score"],ascending=[False,True]),use_container_width=True,hide_index=True)
st.download_button("Download filtered learner summary",student_summary.to_csv(index=False).encode("utf-8"),"student_performance_summary.csv","text/csv")
with st.expander("Metric definitions and responsible use"):
    st.write("All records are synthetic. Pass rate is the share of assessment scores at or above the selected pass mark. Attendance is generated at student level. The review indicator is a transparent sample rule only; it must not be used to rank, label or make automated decisions about real students.")
st.caption("Student Performance Tracking System • Excel portfolio project with an interactive Streamlit companion • Synthetic demonstration data")
