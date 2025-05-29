-- Calculates average number of days between visits per member
SELECT 
    member_id, 
    AVG(DATEDIFF(DAY, LAG(date) OVER (PARTITION BY member_id ORDER BY date), date)) AS avg_days_between_visits
FROM Visits
GROUP BY member_id
ORDER BY avg_days_between_visits;