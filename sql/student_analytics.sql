-- MySQL 8+ | students(student_id,grade,cohort,attendance_pct)
-- assessments(assessment_id,student_id,term,subject,score)
SELECT COUNT(DISTINCT s.student_id) students,ROUND(AVG(a.score),2) average_score,
ROUND(AVG(a.score>=40)*100,2) pass_rate_pct,ROUND(AVG(s.attendance_pct),2) avg_attendance_pct
FROM students s JOIN assessments a USING(student_id);

SELECT term,subject,COUNT(*) assessment_count,ROUND(AVG(score),2) avg_score,
ROUND(AVG(score>=40)*100,2) pass_rate_pct
FROM assessments GROUP BY term,subject ORDER BY term,avg_score DESC;

SELECT CASE WHEN attendance_pct>=90 THEN '90-100%' WHEN attendance_pct>=75 THEN '75-89%' ELSE 'Below 75%' END attendance_band,
COUNT(DISTINCT s.student_id) students,ROUND(AVG(a.score),2) avg_score
FROM students s JOIN assessments a USING(student_id) GROUP BY attendance_band;

-- Transparent support review indicator, not an automated student decision
SELECT s.student_id,s.grade,s.cohort,s.attendance_pct,ROUND(AVG(a.score),2) avg_score,
CASE WHEN s.attendance_pct<75 OR AVG(a.score)<45 THEN 'Review for support' ELSE 'No rule triggered' END review_indicator
FROM students s JOIN assessments a USING(student_id)
GROUP BY s.student_id,s.grade,s.cohort,s.attendance_pct;

SELECT student_id,term,ROUND(AVG(score),2) term_average,
LAG(ROUND(AVG(score),2)) OVER(PARTITION BY student_id ORDER BY term) prior_term_average
FROM assessments GROUP BY student_id,term ORDER BY student_id,term;
