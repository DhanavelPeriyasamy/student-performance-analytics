"""Create fictional student and assessment data for analysis practice."""
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"data"; OUT.mkdir(exist_ok=True)
rng=np.random.default_rng(27); n=900
students=pd.DataFrame({"student_id":range(1,n+1),"grade":rng.choice([9,10,11,12],n),"cohort":rng.choice(["2024-25","2025-26"],n),"attendance_pct":np.round(np.clip(rng.normal(84,11,n),35,100),1)})
rows=[]; aid=1
for s in students.itertuples(index=False):
 for term in [1,2,3]:
  for subject in ["Mathematics","English","Science","Social Studies","Computer Science"]:
   score=float(np.clip(rng.normal(48+(s.attendance_pct-75)*.28,13),0,100))
   rows.append((aid,s.student_id,term,subject,round(score,1))); aid+=1
assessments=pd.DataFrame(rows,columns=["assessment_id","student_id","term","subject","score"])
students.to_csv(OUT/"students.csv",index=False); assessments.to_csv(OUT/"assessments.csv",index=False)
print(f"Generated {len(students)} students and {len(assessments)} assessments")
