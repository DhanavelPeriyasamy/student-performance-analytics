"""Create subject and student-level descriptive summaries."""
from pathlib import Path
import pandas as pd
D=Path(__file__).resolve().parents[1]/"data"
s=pd.read_csv(D/"students.csv"); a=pd.read_csv(D/"assessments.csv")
df=a.merge(s,on="student_id",validate="many_to_one")
subject=(df.groupby(["term","subject"],as_index=False).agg(avg_score=("score","mean"),pass_rate=("score",lambda x:(x>=40).mean()*100),assessment_count=("assessment_id","count")))
subject[["avg_score","pass_rate"]]=subject[["avg_score","pass_rate"]].round(2); subject.to_csv(D/"subject_summary.csv",index=False)
summary=df.groupby("student_id",as_index=False).agg(avg_score=("score","mean"),attendance_pct=("attendance_pct","first"))
summary["support_review_flag"]=(summary.avg_score<45)|(summary.attendance_pct<75)
summary.to_csv(D/"student_summary.csv",index=False)
print(subject.to_string(index=False))
print("Students requiring human review:",int(summary.support_review_flag.sum()))
