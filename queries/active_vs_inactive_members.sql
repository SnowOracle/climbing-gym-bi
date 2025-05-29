-- Compares the number of active vs. inactive members
SELECT is_active, COUNT(*) AS total_members
FROM Members
GROUP BY is_active;