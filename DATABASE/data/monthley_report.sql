INSERT INTO engagement_logs 
(organisation_id, user_id, engagement_type, created_at)
VALUES
(159, 366, 'view', '2026-05-01'),
(159, 366, 'view', '2026-05-02'),
(159, 366, 'save', '2026-05-03'),
(159, 366, 'message', '2026-05-04'),
(159, 366, 'review', '2026-05-05');




INSERT INTO engagement_logs 
(organisation_id, user_id, engagement_type, created_at)
VALUES
(159, 1, 'profile_view', '2026-06-01'),
(159, 2, 'profile_view', '2026-06-02'),
(159, 3, 'profile_view', '2026-06-03'),
(159, 2, 'save', '2026-06-04'),
(159, 3, 'save', '2026-06-05'),
(159, 3, 'message', '2026-06-06'),
(159, 2, 'rating', '2026-06-07'),
(159, 2, 'volunteer_signup', '2026-06-08');


CREATE VIEW organisation_monthly_report_view AS
SELECT
    o.organisation_name,
    m.organisation_id,
    m.report_month,
    m.report_year,
    m.total_views,
    m.total_saves,
    m.total_messages,
    m.total_reviews,
    m.total_volunteer_signups,
    m.average_rating,
    m.bayesian_rating,
    m.engagement_score,
    m.trend_score,
    m.growth_rate,
    m.trend_status,
    m.generated_at
FROM monthly_business_reports m
JOIN organisations o
    ON m.organisation_id = o.organisation_id;
    
    

SELECT *
FROM organisation_monthly_report_view
WHERE organisation_id = 159
ORDER BY report_year, report_month;
