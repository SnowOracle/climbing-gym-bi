import os

output_dir = "/Users/gsvsleeperservice/PycharmProjects/climbing_BI/queries"

queries = {
    "members_by_age_group.sql": """
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
""",
    "visits_per_month.sql": """
-- Shows how many visits each member made per month
SELECT 
    FORMAT(date, 'yyyy-MM') AS visit_month,
    member_id,
    COUNT(*) AS total_visits
FROM Visits
GROUP BY FORMAT(date, 'yyyy-MM'), member_id
ORDER BY visit_month DESC, total_visits DESC;
""",
    "top_buyers.sql": """
-- Lists the top 10 customers by total spending
SELECT customer_id, COUNT(*) AS total_purchases, SUM(price) AS total_spent
FROM Sales
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;
""",
    "sales_by_item.sql": """
-- Shows how many times each item was sold
SELECT item, COUNT(*) AS times_sold
FROM Sales
GROUP BY item
ORDER BY times_sold DESC;
""",
    "avg_visit_duration.sql": """
-- Lists members with the longest average visit duration
SELECT member_id, AVG(duration) AS avg_duration
FROM Visits
GROUP BY member_id
ORDER BY avg_duration DESC
LIMIT 10;
""",
    "revenue_by_month.sql": """
-- Sums up total sales revenue by month
SELECT 
    FORMAT(date, 'yyyy-MM') AS sales_month,
    SUM(price) AS total_revenue
FROM Sales
GROUP BY FORMAT(date, 'yyyy-MM')
ORDER BY sales_month DESC;
""",
    "active_vs_inactive_members.sql": """
-- Compares the number of active vs. inactive members
SELECT is_active, COUNT(*) AS total_members
FROM Members
GROUP BY is_active;
""",
    "weekday_popularity.sql": """
-- Shows which days of the week have the most visits
SELECT 
    DATEPART(WEEKDAY, date) AS weekday, 
    COUNT(*) AS visit_count
FROM Visits
GROUP BY DATEPART(WEEKDAY, date)
ORDER BY visit_count DESC;
""",
    "buyers_who_never_visited.sql": """
-- Finds customers who bought something but never visited
SELECT DISTINCT s.customer_id
FROM Sales s
LEFT JOIN Visits v ON s.customer_id = v.member_id
WHERE v.member_id IS NULL;
""",
    "average_days_between_visits.sql": """
-- Calculates average number of days between visits per member
SELECT 
    member_id, 
    AVG(DATEDIFF(DAY, LAG(date) OVER (PARTITION BY member_id ORDER BY date), date)) AS avg_days_between_visits
FROM Visits
GROUP BY member_id
ORDER BY avg_days_between_visits;
""",
    "spending_vs_visits.sql": """
-- Compares visit frequency and total spending per member
SELECT 
    v.member_id,
    COUNT(v.visit_id) AS total_visits,
    SUM(s.price) AS total_spent
FROM Visits v
JOIN Sales s ON v.member_id = s.member_id
GROUP BY v.member_id
ORDER BY total_spent DESC;
""",
    "day_pass_vs_member_usage.sql": """
-- Compares how many people used memberships vs. day passes
SELECT 
    (SELECT COUNT(*) FROM Visits) AS total_member_visits,
    (SELECT COUNT(*) FROM Day_Passes) AS total_day_pass_visits;
"""
}

# Create folder if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Save each query to a .sql file
for filename, sql in queries.items():
    with open(os.path.join(output_dir, filename), "w") as f:
        f.write(sql.strip())

print(f"✅ All queries saved to {output_dir}")
