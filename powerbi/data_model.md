# Power BI model and report guide
Students: one row per fictional learner with grade, cohort and attendance. Assessments: one row per student-subject-term assessment. Create a one-to-many relationship Students[student_id] to Assessments[student_id], with single-direction filtering.

Pages: (1) Academic overview—student count, average score, pass rate and attendance. (2) Subject performance—subject average and pass rate by term. (3) Cohort comparison—grade/cohort comparisons with sample sizes. (4) Support review—transparent rule triggers, with student-level drill-through restricted to authorized viewers.

Show the score scale and pass threshold. Do not publish identifiable learner data or treat support flags as predictions.
