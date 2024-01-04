-- Test 1 for employees
SELECT COUNT(*) FROM employees WHERE Address IS NOT NULL HAVING COUNT(*) = 2;
