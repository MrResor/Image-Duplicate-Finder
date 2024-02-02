-- SQLite
SELECT id, path
FROM images
WHERE id IN (
    SELECT id 
    FROM images
    GROUP BY id
    HAVING COUNT(*) > 1)
ORDER BY id;