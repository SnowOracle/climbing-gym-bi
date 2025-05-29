-- Lists members with the longest average visit duration
SELECT member_id, AVG(duration) AS avg_duration
FROM Visits
GROUP BY member_id
ORDER BY avg_duration DESC
LIMIT 10;