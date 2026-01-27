-- SQL script to delete all academic batches
-- This will cascade delete all related records (years, semesters, sections, labs, subjects)

-- Show what will be deleted
SELECT 'Batches to be deleted:' as info;
SELECT id, batch_code, batch_name, joining_year, total_students 
FROM academic_batches 
ORDER BY id;

-- Uncomment the line below to actually delete (after reviewing above)
-- DELETE FROM academic_batches;

-- To run this script:
-- 1. Get your database URL from apps/api/.env
-- 2. Run: psql "YOUR_DATABASE_URL" -f delete_batches.sql
-- 
-- OR if you have the connection details:
-- psql -h hostname -U username -d database_name -f delete_batches.sql
