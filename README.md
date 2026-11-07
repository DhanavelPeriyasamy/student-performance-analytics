# Student Performance & Academic Risk Analytics

A reproducible analytics project for exploring academic outcomes, attendance, assessment performance, and student support indicators. The workflow generates fictional student records, validates data quality, calculates cohort and subject KPIs, and provides SQL and Power BI assets for reporting.

> **Privacy:** All generated records are synthetic. Do not commit identifiable student data, grades, or education records without explicit authorization and appropriate safeguards.

## Business questions
- How do scores and pass rates vary by subject, grade, and term?
- Is attendance associated with academic performance?
- Which students may benefit from early academic support?
- How do cohorts progress across assessment periods?
- Which subjects show the widest performance gaps?

## KPI definitions
| KPI | Definition |
|---|---|
| Average score | Mean assessment score |
| Pass rate | Assessments at or above the configured pass mark / valid assessments |
| Attendance % | Sessions attended / sessions held × 100 |
| At-risk indicator | Rule-based flag using low attendance and/or low average score |
| Subject gap | Difference between highest and lowest subject average |

The at-risk flag is an exploratory support indicator, not a definitive prediction or a label of student ability.

## Structure
```text
├── README.md
├── requirements.txt
├── data/                       # generated CSVs (ignored)
├── src/
│   ├── generate_data.py
│   └── analyze_performance.py
├── sql/
│   └── student_analytics.sql
├── powerbi/
│   ├── data_model.md
│   └── dax_measures.dax
└── docs/
    └── interpretation.md
```

## Quick start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/generate_data.py
python src/analyze_performance.py
```

## Dashboard blueprint
1. **Academic overview:** student count, average score, pass rate, attendance.
2. **Subject analysis:** subject averages, pass rates, score distribution.
3. **Cohort analysis:** grade and term comparisons.
4. **Student support:** transparent rule-based indicators with drill-through restricted to authorized users.

## Analytical safeguards
- Do not rank or stigmatize students using a single metric.
- Display sample sizes and missing-data coverage.
- Compare like-for-like cohorts and assessment scales.
- Use support flags to prompt human review, not automated decisions.
- Keep personally identifiable information out of public repositories.

## Skills demonstrated
Excel-style KPI logic, Python/Pandas, data cleaning, descriptive statistics, SQL grouping and window functions, Power BI modeling, DAX, and data storytelling.

## Author
**Dhanavel Periyasamy** · Data Analytics Portfolio

## Interactive web dashboard

The repository includes a browser-based Streamlit dashboard in `app.py`. It provides cohort, grade, subject and term filters, academic KPI cards, interactive score and attendance charts, a transparent support-review rule, and CSV export.

### Publish the dashboard

1. Open [Streamlit Community Cloud](https://share.streamlit.io/) and sign in with the GitHub account that owns this repository.
2. Select **Create app** and choose **Yup, I have an app**.
3. Set repository to `DhanavelPeriyasamy/student-performance-analytics`, branch to `main`, and main file path to `app.py`.
4. Choose a memorable app URL if available, then select **Deploy**.
5. When deployment finishes, copy the public app URL into your resume and this README.

The app creates its synthetic CSV data on first launch if the files are not present. All student records are fictional. See [Streamlit's deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).
