-- Get the maximum average squared acceleration in the z-coordinate over all of the segments
SELECT MAX(b.avg_accel)
FROM (
    SELECT s.uid as uid, s.ts2 as ts2, AVG(z_accel * z_accel) as avg_accel
    FROM segments s, accelerometer a
    WHERE s.uid = a.user_id AND a.time_stamp <= s.ts2 and a.time_stamp >= s.ts1
    GROUP BY s.uid, s.ts2
    ) b;