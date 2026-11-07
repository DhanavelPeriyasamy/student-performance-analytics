-- Student Performance Analytics | MySQL 8+
-- Tables: students(student_id, grade, cohort, attendance_pct)
-- assessments(assessment_id, student_id, term, subject, score)

-- 1. Overall academic KPIs
SELECT COUNT(DISTINCT s.student_id) AS students,
       ROUND(AVG(a.score),2) AS average_score,
       ROUND(AVG(a.score >= 40)*100,2) AS pass_rate_pct,
       ROUND(AVG(s.attendance_pct),2) AS avg_attendance_pct
FROM students s JOIN assessments a USING(student_id);

-- 2. Subject and term performance
SELECT term, subject, COUNT(*) AS assessment_count,
       ROUND(AVG(score),2) AS avg_score,
       ROUND(AVG(score >= 40)*100,2) AS pass_rate_pct
FROM assessments GROUP BY term, subject ORDER BY term, avg_score DESC;

-- 3. Attendance bands and outcomes
SELECT CASE WHEN attendance_pct >= 90 THEN '90-100%'
            WHEN attendance_pct >= 75 THEN '75-89%'
            ELSE 'Below 75%' END AS attendance_band,
       COUNT(DISTINCT s.student_id) AS students,
       ROUND(AVG(a.score),2) AS avg_score
FROM students s JOIN assessments a USING(student_id)
GROUP BY attendance_band ORDER BY MIN(attendance_pct) DESC;

-- 4. Transparent support-review list; not an automated decision
SELECT s.student_id, s.grade, s.cohort, s.attendance_pct,
       ROUND(AVG(a.score),2) AS avg_score,
       CASE WHEN s.attendance_pct < 75 OR AVG(a.score) < 45
            THEN 'Review for support' ELSE 'No rule triggered' END AS review_indicator
FROM students s JOIN assessments a USING(student_id)
GROUP BY s.student_id,s.grade,s.cohort,s.attendance_pct;

-- 5. Student score trend by term
SELECT student_id, term, ROUND(AVG(score),2) AS term_average,
       LAG(ROUND(AVG(score),2)) OVER (PARTITION BY student_id ORDER BY term) AS prior_term_average
FROM assessments GROUP BY student_id,term ORDER BY student_id,term;
