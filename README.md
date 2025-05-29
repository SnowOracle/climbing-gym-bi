# Climbing Gym Business Intelligence System

A comprehensive business intelligence system for climbing gyms that simulates and analyzes customer data, membership information, visits, day passes, and sales.

## Overview

This project provides tools for:
1. Generating realistic simulated data for a climbing gym business
2. Managing and inserting data into a SQL Server database
3. Running business intelligence queries for data analysis
4. Visualizing key performance indicators

## Features

- **Data Simulation**: Generate realistic customer, member, visit, day pass, and sales data
- **Database Integration**: Store and manage data in SQL Server
- **Business Intelligence**: SQL queries to extract valuable insights including:
  - Member activity analysis
  - Visit patterns and duration
  - Sales and revenue reporting
  - Customer segmentation
  - Day pass vs. membership usage
- **Sample Data**: Includes pre-generated CSV files as working examples (customers, members, visits, day passes, sales)

## Tech Stack

- Python 3.x
- Pandas for data manipulation
- pyODBC for SQL Server connectivity
- SQL Server database

## Setup

### Prerequisites

- Python 3.x
- SQL Server instance (local or remote)
- Required Python packages: pandas, numpy, pyodbc

### Database Configuration

Configure your database connection in `test_db.py`:

```python
server = '127.0.0.1'  # Your SQL Server instance
port = '1433'
database = 'test_db'  # Target database
username = 'climbing_user'  # SQL Server user
password = 'hoosierheights'  # Password
driver = '/opt/homebrew/lib/libtdsodbc.so'  # Driver path
```

## Usage

### Data Generation

Generate sample data:

```bash
python data_generation_2.py
```

### Database Operations

Insert data into the database:

```bash
python data_insert_handling_2.py
```

Clear tables if needed:

```bash
python truncate_tables.py
```

### Running Queries

The `queries` folder contains SQL queries that deliver critical business insights. Here are 10 examples with their business value:

#### 1. Active vs Inactive Member Analysis
```sql
-- Compares the number of active vs. inactive members
SELECT is_active, COUNT(*) AS total_members
FROM Members
GROUP BY is_active;
```
**Business Value:** Allows managers to track membership retention rates and identify periods of increased churn, helping to evaluate the effectiveness of membership renewal campaigns.

#### 2. Age Demographics Analysis
```sql
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
```
**Business Value:** Helps tailor marketing efforts, class schedules, and facility amenities to match the gym's primary demographic groups, maximizing relevance and appeal.

#### 3. Monthly Revenue Tracking
```sql
-- Sums up total sales revenue by month
SELECT 
    FORMAT(date, 'yyyy-MM') AS sales_month,
    SUM(price) AS total_revenue
FROM Sales
GROUP BY FORMAT(date, 'yyyy-MM')
ORDER BY sales_month DESC;
```
**Business Value:** Provides clear visibility into monthly revenue patterns, helping management identify seasonal trends and measure the impact of promotional campaigns.

#### 4. Top Spenders Identification
```sql
-- Lists the top 10 customers by total spending
SELECT customer_id, COUNT(*) AS total_purchases, SUM(price) AS total_spent
FROM Sales
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;
```
**Business Value:** Identifies the most valuable customers for personalized retention efforts, loyalty rewards, and VIP services to maximize lifetime customer value.

#### 5. Visit Duration Analysis
```sql
-- Lists members with the longest average visit duration
SELECT member_id, AVG(duration) AS avg_duration
FROM Visits
GROUP BY member_id
ORDER BY avg_duration DESC
LIMIT 10;
```
**Business Value:** Helps understand facility usage patterns, potentially influencing decisions on extending hours or adding amenities that encourage longer visits and greater engagement.

#### 6. Day Pass vs Membership Usage
```sql
-- Compares how many people used memberships vs. day passes
SELECT 
    (SELECT COUNT(*) FROM Visits) AS total_member_visits,
    (SELECT COUNT(*) FROM Day_Passes) AS total_day_pass_visits;
```
**Business Value:** Provides insights for pricing strategy by comparing the popularity of day passes versus memberships, helping optimize the business model.

#### 7. Weekday Popularity Analysis
```sql
-- Shows which days of the week have the most visits
SELECT 
    DATEPART(WEEKDAY, date) AS weekday, 
    COUNT(*) AS visit_count
FROM Visits
GROUP BY DATEPART(WEEKDAY, date)
ORDER BY visit_count DESC;
```
**Business Value:** Guides staffing decisions and special event scheduling by identifying peak days, ensuring appropriate resource allocation and maximizing revenue opportunities.

#### 8. Visit Frequency Analysis
```sql
-- Calculates average number of days between visits per member
SELECT 
    member_id, 
    AVG(DATEDIFF(DAY, LAG(date) OVER (PARTITION BY member_id ORDER BY date), date)) AS avg_days_between_visits
FROM Visits
GROUP BY member_id
ORDER BY avg_days_between_visits;
```
**Business Value:** Identifies at-risk members who visit infrequently, enabling proactive retention efforts before they cancel their memberships.

#### 9. Conversion Opportunity Identification
```sql
-- Finds customers who bought something but never visited
SELECT DISTINCT s.customer_id
FROM Sales s
LEFT JOIN Visits v ON s.customer_id = v.member_id
WHERE v.member_id IS NULL;
```
**Business Value:** Reveals potential customers who have shown interest by making purchases but haven't become gym visitors, creating targeted conversion opportunities.

#### 10. Spending vs Visit Correlation
```sql
-- Compares visit frequency and total spending per member
SELECT 
    v.member_id,
    COUNT(v.visit_id) AS total_visits,
    SUM(s.price) AS total_spent
FROM Visits v
JOIN Sales s ON v.member_id = s.member_id
GROUP BY v.member_id
ORDER BY total_spent DESC;
```
**Business Value:** Reveals the relationship between visit frequency and spending, helping management create effective cross-selling strategies and targeted promotions.

#### 11. Advanced Customer Lifetime Value Analysis
```sql
-- Complex query using CTEs and window functions to calculate customer lifetime value
-- and predict future value based on visit patterns and spending habits

WITH MemberMetrics AS (
    -- First CTE: Calculate base metrics for each member
    SELECT 
        m.member_id,
        m.customer_id,
        m.name,
        m.age,
        m.join_date,
        m.is_active,
        DATEDIFF(DAY, m.join_date, GETDATE()) AS days_as_member,
        COUNT(DISTINCT v.visit_id) AS total_visits,
        CASE WHEN COUNT(DISTINCT v.visit_id) > 0 
             THEN DATEDIFF(DAY, m.join_date, GETDATE()) / CAST(COUNT(DISTINCT v.visit_id) AS FLOAT) 
             ELSE NULL END AS days_between_visits
    FROM 
        Members m
    LEFT JOIN 
        Visits v ON m.member_id = v.member_id
    GROUP BY 
        m.member_id, m.customer_id, m.name, m.age, m.join_date, m.is_active
),

SpendingPatterns AS (
    -- Second CTE: Calculate spending patterns
    SELECT 
        mm.member_id,
        mm.customer_id,
        COALESCE(SUM(s.price), 0) AS total_spending,
        COALESCE(COUNT(s.sale_id), 0) AS transaction_count,
        CASE WHEN mm.days_as_member > 0 
             THEN COALESCE(SUM(s.price), 0) / mm.days_as_member * 30 
             ELSE 0 END AS monthly_spend_rate,
        COALESCE(AVG(s.price), 0) AS avg_transaction_value
    FROM 
        MemberMetrics mm
    LEFT JOIN 
        Sales s ON mm.customer_id = s.customer_id
    GROUP BY 
        mm.member_id, mm.customer_id, mm.days_as_member
),

EngagementScore AS (
    -- Third CTE: Calculate engagement score
    SELECT 
        mm.member_id,
        mm.customer_id,
        mm.name,
        mm.age,
        mm.is_active,
        mm.total_visits,
        sp.total_spending,
        sp.monthly_spend_rate,
        -- Recency Factor (based on days since last visit)
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM Visits v 
                WHERE v.member_id = mm.member_id 
                AND DATEDIFF(DAY, v.date, GETDATE()) <= 14
            ) THEN 3  -- Visited in last 14 days
            WHEN EXISTS (
                SELECT 1 FROM Visits v 
                WHERE v.member_id = mm.member_id 
                AND DATEDIFF(DAY, v.date, GETDATE()) <= 30
            ) THEN 2  -- Visited in last 30 days
            WHEN EXISTS (
                SELECT 1 FROM Visits v 
                WHERE v.member_id = mm.member_id
            ) THEN 1  -- Has visited before
            ELSE 0    -- Never visited
        END AS recency_score,
        
        -- Frequency Score (based on visit frequency)
        CASE 
            WHEN mm.total_visits >= 20 THEN 3  -- High frequency
            WHEN mm.total_visits >= 10 THEN 2  -- Medium frequency
            WHEN mm.total_visits >= 1 THEN 1   -- Low frequency
            ELSE 0                             -- No visits
        END AS frequency_score,
        
        -- Monetary Score (based on spending)
        CASE 
            WHEN sp.total_spending >= 500 THEN 3  -- High spender
            WHEN sp.total_spending >= 200 THEN 2  -- Medium spender
            WHEN sp.total_spending > 0 THEN 1     -- Low spender
            ELSE 0                                -- No spending
        END AS monetary_score
    FROM 
        MemberMetrics mm
    JOIN 
        SpendingPatterns sp ON mm.member_id = sp.member_id
)

-- Final query: Calculate Customer Lifetime Value with segment classification
SELECT 
    es.member_id,
    es.name,
    es.age,
    es.is_active,
    es.total_visits,
    es.total_spending,
    es.monthly_spend_rate,
    
    -- Calculate RFM (Recency, Frequency, Monetary) Score
    (es.recency_score + es.frequency_score + es.monetary_score) AS rfm_score,
    
    -- Estimate 12-month Customer Lifetime Value
    CASE WHEN es.is_active = 1 
         THEN es.monthly_spend_rate * 12 * (1 + (es.frequency_score * 0.1))
         ELSE 0 
    END AS projected_annual_value,
    
    -- Segment members into value categories
    CASE 
        WHEN (es.recency_score + es.frequency_score + es.monetary_score) >= 7 THEN 'Premium'
        WHEN (es.recency_score + es.frequency_score + es.monetary_score) >= 4 THEN 'Core'
        WHEN (es.recency_score + es.frequency_score + es.monetary_score) >= 1 THEN 'Casual'
        ELSE 'At Risk'
    END AS customer_segment,
    
    -- Churn probability based on activity patterns
    CASE 
        WHEN es.is_active = 0 THEN 1.0  -- Already churned
        WHEN es.recency_score = 0 THEN 0.8  -- No recent visits
        WHEN es.recency_score = 1 THEN 0.5  -- Low recency
        WHEN es.recency_score = 2 THEN 0.2  -- Medium recency
        ELSE 0.1  -- High recency
    END AS churn_probability
FROM 
    EngagementScore es
ORDER BY 
    projected_annual_value DESC;
```

**Business Value:** This advanced analysis delivers multiple strategic insights:
1. **Customer Lifetime Value Calculation** - Estimates future revenue from each customer based on their current patterns
2. **Customer Segmentation** - Classifies members into Premium, Core, Casual, and At-Risk categories for targeted marketing
3. **Churn Prediction** - Identifies members with high probability of cancellation, enabling preemptive retention actions
4. **Revenue Forecasting** - Projects future revenue based on current member behavior
5. **Marketing ROI Potential** - Helps determine appropriate acquisition costs for different customer segments

By using CTEs, window functions, and sophisticated scoring algorithms, this query transforms raw transaction data into actionable business intelligence for strategic decision-making.

## Project Structure

```
climbing_BI/
├── data_generation.py         # Initial data generation script
├── data_generation_2.py       # Enhanced data generation script
├── data_insert_handling.py    # Initial data insertion script
├── data_insert_handling_2.py  # Enhanced data insertion script
├── main.py                    # Entry point
├── query_writer.py            # Utility for writing SQL queries
├── test_db.py                 # Database connection testing
├── truncate_tables.py         # Utility to clear database tables
├── queries/                   # SQL queries for analysis
│   ├── active_vs_inactive_members.sql
│   ├── average_days_between_visits.sql
│   ├── ...
├── *.csv                      # Generated data files
```

## License

[MIT License](https://opensource.org/licenses/MIT)

## Contact

Your Name - [Your Email or LinkedIn] 