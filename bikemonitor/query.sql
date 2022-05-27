-- Return a segment of a trip with the average squared magnitude of acceleration over that segment
-- Also include the start and end points of that segment
SELECT lat1, lon1, lat2, lon2, AVG(x_accel * x_accel + y_accel * y_accel + z_accel * z_accel)
FROM (
    -- For each location data instance, find the previous coordinates and time_stamp within the same trip
    SELECT l.user_id as uid, l.time_stamp as ts2, m.time_stamp as ts1, l.latitude as lat2, l.longitude as lon2, m.latitude as lat1, m.longitude as lon1
    FROM locations l, locations m
    WHERE l.user_id = m.user_id AND l.trip_id = m.trip_id AND m.time_stamp = (
        -- Find previous time_stamp
        SELECT MAX(time_stamp) 
        FROM locations n 
        WHERE n.user_id = l.user_id AND n.trip_id = l.trip_id AND n.time_stamp < l.time_stamp
    )
) b, accelerometer a
WHERE b.uid = a.user_id AND a.time_stamp <= b.ts2 and a.time_stamp >= b.ts1
GROUP BY b.uid, b.ts2
LIMIT 1000;