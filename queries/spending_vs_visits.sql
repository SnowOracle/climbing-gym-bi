-- Compares visit frequency and total spending per member
SELECT 
    v.member_id,
    COUNT(v.visit_id) AS total_visits,
    SUM(s.price) AS total_spent
FROM Visits v
JOIN Sales s ON v.member_id = s.member_id
GROUP BY v.member_id
ORDER BY total_spent DESC;