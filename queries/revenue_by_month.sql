-- Sums up total sales revenue by month
SELECT 
    FORMAT(date, 'yyyy-MM') AS sales_month,
    SUM(price) AS total_revenue
FROM Sales
GROUP BY FORMAT(date, 'yyyy-MM')
ORDER BY sales_month DESC;