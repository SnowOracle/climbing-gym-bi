-- Shows how many visits each member made per month
SELECT 
    FORMAT(date, 'yyyy-MM') AS visit_month,
    member_id,
    COUNT(*) AS total_visits
FROM Visits
GROUP BY FORMAT(date, 'yyyy-MM'), member_id
ORDER BY visit_month DESC, total_visits DESC;