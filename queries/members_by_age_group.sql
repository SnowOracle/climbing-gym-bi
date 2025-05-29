-- Groups members into age brackets and counts how many fall into each
SELECT 
    CASE 
        WHEN age BETWEEN 5 AND 17 THEN 'Under 18'
        WHEN age BETWEEN 18 AND 25 THEN '18-25'
        WHEN age BETWEEN 26 AND 35 THEN '26-35'
        WHEN age BETWEEN 36 AND 45 THEN '36-45'
        WHEN age > 45 THEN '46+'
    END AS age_group,
    COUNT(*) AS total_members
FROM Members
GROUP BY 
    CASE 
        WHEN age BETWEEN 5 AND 17 THEN 'Under 18'
        WHEN age BETWEEN 18 AND 25 THEN '18-25'
        WHEN age BETWEEN 26 AND 35 THEN '26-35'
        WHEN age BETWEEN 36 AND 45 THEN '36-45'
        WHEN age > 45 THEN '46+'
    END
ORDER BY total_members DESC;