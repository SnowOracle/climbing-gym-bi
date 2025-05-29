-- Lists the top 10 customers by total spending
SELECT customer_id, COUNT(*) AS total_purchases, SUM(price) AS total_spent
FROM Sales
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;