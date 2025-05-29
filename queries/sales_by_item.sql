-- Shows how many times each item was sold
SELECT item, COUNT(*) AS times_sold
FROM Sales
GROUP BY item
ORDER BY times_sold DESC;