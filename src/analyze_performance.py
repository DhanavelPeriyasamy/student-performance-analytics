"""Summarize synthetic student assessment and attendance data."""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
students = pd.read_csv(DATA/"students.csv")
assessments = pd.read_csv(DATA/"assessments.csv")
df = assessments.merge(students,on="student_id",validate="many_to_one")
summary = (df.groupby(["term","subject"],as_index=False)
             .agg(avg_score=("score","mean"),
                  pass_rate=("score",lambda x:(x>=40).mean()*100),
                  assessment_count=("assessment_id","count")))
summary[["avg_score","pass_rate"]] = summary[["avg_score","pass_rate"]].round(2)
summary.to_csv(DATA/"subject_summary.csv",index=False)

student_summary = (df.groupby("student_id",as_index=False)
    .agg(avg_score=("score","mean"), attendance_pct=("attendance_pct","first")))
student_summary["support_review_flag"] = (
    (student_summary["avg_score"] < 45) | (student_summary["attendance_pct"] < 75)
)
student_summary.to_csv(DATA/"student_summary.csv",index=False)
print("Subject summary:")
print(summary.to_string(index=False))
print(f"Students flagged for human support review: {student_summary.support_review_flag.sum()}")
