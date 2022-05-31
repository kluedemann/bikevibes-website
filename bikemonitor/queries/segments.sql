CREATE VIEW IF NOT EXISTS segments(uid, tid, ts1, lat1, lon1, ts2, lat2, lon2)
AS
    SELECT l.user_id, l.trip_id, m.time_stamp, m.latitude, m.longitude, l.time_stamp, l.latitude, l.longitude
    FROM locations l, locations m
    WHERE l.user_id = m.user_id AND l.trip_id = m.trip_id AND m.time_stamp = (
        SELECT MAX(time_stamp) 
        FROM locations n 
        WHERE n.user_id = l.user_id AND n.trip_id = l.trip_id AND n.time_stamp < l.time_stamp
    );

