-- Test 1 for customers
SELECT CustomerId, COUNT(*) FROM customers GROUP BY CustomerId HAVING COUNT(*) > 1;
