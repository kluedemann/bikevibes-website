-- Get the endpoints and average squared acceleration of each segment
-- Only consider the 1000 most recent
SELECT g.lat1, g.lon1, g.lat2, g.lon2, b.avg_accel
FROM (
    -- Get average squared acceleration of each segment
    SELECT s.uid as uid, s.ts2 as ts2, AVG(x_accel * x_accel + y_accel * y_accel + z_accel * z_accel) as avg_accel
    FROM segments s, accelerometer a
    WHERE s.uid = a.user_id AND a.time_stamp <= s.ts2 and a.time_stamp >= s.ts1
    GROUP BY s.uid, s.ts2
    ORDER BY s.ts2 DESC
    LIMIT 1000
    ) b, segments g
WHERE g.uid = b.uid AND g.ts2 = b.ts2;
