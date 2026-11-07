# Power BI model and report guide

## Model
- **Students**: one row per synthetic student, including grade, cohort, attendance.
- **Assessments**: one row per student-subject-term assessment.
- **Subjects**: optional dimension created from distinct subject names.
- **Terms**: optional term dimension.

Create a one-to-many relationship Students[student_id] → Assessments[student_id]. Keep filters single-direction unless a documented requirement justifies otherwise.

## Pages
1. Academic overview: distinct students, average score, pass rate, average attendance.
2. Subject performance: average score and pass rate by subject and term.
3. Cohort comparison: grade/cohort comparisons with sample-size context.
4. Support review: rule-trigger counts and drill-through with appropriate access controls.

Use consistent score scales and show the pass threshold. Do not publish identifiable student-level detail.
