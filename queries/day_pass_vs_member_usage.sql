-- Compares how many people used memberships vs. day passes
SELECT 
    (SELECT COUNT(*) FROM Visits) AS total_member_visits,
    (SELECT COUNT(*) FROM Day_Passes) AS total_day_pass_visits;