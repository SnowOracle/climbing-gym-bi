-- Finds customers who bought something but never visited
SELECT DISTINCT s.customer_id
FROM Sales s
LEFT JOIN Visits v ON s.customer_id = v.member_id
WHERE v.member_id IS NULL;