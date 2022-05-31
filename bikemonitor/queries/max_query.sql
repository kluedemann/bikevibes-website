-- Get the maximum average squared acceleration over all of the segments
-- Only consider the 1000 most recent segments
SELECT MAX(b.avg_accel)
FROM (
    SELECT s.uid as uid, s.ts2 as ts2, AVG(x_accel * x_accel + y_accel * y_accel + z_accel * z_accel) as avg_accel
    FROM segments s, accelerometer a
    WHERE s.uid = a.user_id AND a.time_stamp <= s.ts2 and a.time_stamp >= s.ts1
    GROUP BY s.uid, s.ts2
    ORDER BY s.ts2 DESC
    LIMIT 1000
    ) b;