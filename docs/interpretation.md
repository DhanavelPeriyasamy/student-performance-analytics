# Interpretation and responsible use

## Workflow
1. Generate the synthetic students and assessment rows.
2. Run the Python analysis to produce subject and student summaries.
3. Run the SQL queries in MySQL 8+.
4. Build the Power BI model and measures.
5. Compare subjects and terms, then investigate patterns with cohort context.

## Interpretation
Attendance and assessment outcomes may be associated in this synthetic dataset because the generator deliberately includes a modest relationship. This is not causal evidence. The rule-based support flag is intended to demonstrate transparent analytics, not to classify a learner's potential or trigger automated interventions.

Always show sample sizes, explain the pass threshold, account for missing assessments, and involve educators when interpreting student-level patterns. Never use public dashboards to expose student identities or grades.
