"""Generate fictional academic data for the portfolio project."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = np.random.default_rng(27)
n = 900
students = pd.DataFrame({
    "student_id": np.arange(1,n+1),
    "grade": rng.choice([9,10,11,12],n),
    "cohort": rng.choice(["2024-25","2025-26"],n),
    "attendance_pct": np.round(np.clip(rng.normal(84,11,n),35,100),1)
})
students.to_csv(DATA/"students.csv",index=False)
subjects = ["Mathematics","English","Science","Social Studies","Computer Science"]
rows=[]
assessment_id=1
for s in students.itertuples(index=False):
    for term in [1,2,3]:
        for subject in subjects:
            # Attendance contributes modestly to the synthetic score, with noise.
            score = np.clip(rng.normal(48 + (s.attendance_pct-75)*.28, 13), 0, 100)
            rows.append((assessment_id,s.student_id,term,subject,round(float(score),1)))
            assessment_id += 1
assessments = pd.DataFrame(rows,columns=["assessment_id","student_id","term","subject","score"])
assessments.to_csv(DATA/"assessments.csv",index=False)
print(f"Created {len(students):,} students and {len(assessments):,} assessment rows in {DATA}")
