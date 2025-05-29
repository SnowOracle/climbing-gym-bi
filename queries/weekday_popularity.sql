-- Shows which days of the week have the most visits
SELECT 
    DATEPART(WEEKDAY, date) AS weekday, 
    COUNT(*) AS visit_count
FROM Visits
GROUP BY DATEPART(WEEKDAY, date)
ORDER BY visit_count DESC;