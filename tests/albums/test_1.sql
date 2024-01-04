-- Test 1 for albums
SELECT COUNT(*) FROM albums WHERE Title IS NOT NULL HAVING COUNT(*) = 2;
