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






INSERT INTO monthly_business_reports
(
    organisation_id,
    report_month,
    report_year,
    total_views,
    total_saves,
    total_messages,
    total_reviews,
    total_volunteer_signups,
    engagement_score,
    growth_rate,
    trend_status
)
SELECT
    1 AS organisation_id,
    5 AS report_month,
    2026 AS report_year,

    COUNT(*) FILTER (WHERE engagement_type = 'view') AS total_views,
    COUNT(*) FILTER (WHERE engagement_type = 'save') AS total_saves,
    COUNT(*) FILTER (WHERE engagement_type = 'message') AS total_messages,
    COUNT(*) FILTER (WHERE engagement_type = 'review') AS total_reviews,
    COUNT(*) FILTER (WHERE engagement_type = 'volunteer_signup') AS total_volunteer_signups,

    (
        COUNT(*) FILTER (WHERE engagement_type = 'view') * 1
        + COUNT(*) FILTER (WHERE engagement_type = 'save') * 3
        + COUNT(*) FILTER (WHERE engagement_type = 'message') * 4
        + COUNT(*) FILTER (WHERE engagement_type = 'review') * 5
        + COUNT(*) FILTER (WHERE engagement_type = 'volunteer_signup') * 5
    ) AS engagement_score,

    0 AS growth_rate,
    'New / Base Month' AS trend_status

FROM engagement_logs
WHERE organisation_id = 1
  AND created_at >= '2026-05-01'
  AND created_at < '2026-06-01';
