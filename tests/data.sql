INSERT INTO locations (user_id, time_stamp, trip_id, latitude, longitude)
VALUES
    ('test', 0, 0, 53.52639, -113.52548),
    ('test', 1, 0, 53.51, -113.4938),
    ('test', 2, 0, 53.54, -113.4938),
    ('test', 3, 1, 53.5, -113.45),
    ('test', 4, 1, 53.52, -113.48),
    ('test2', 0, 0, 53.55, -113.5),
    ('test2', 1, 0, 53.57, -113.52),
    ('test', 5, 2, 53.48, -113.55),
    ('test', 6, 3, 53.46, -113.57),
    ('test', 7, 3, 53.6, -113.52);

INSERT INTO accelerometer (user_id, time_stamp, trip_id, x_accel, y_accel, z_accel)
VALUES 
    ('test', 0, 0, 1.0, 1.0, 2.0),
    ('test', 1, 0, 10.0, 10.0, 10.0),
    ('test', 2, 0, 17.0, 0.0, 0.0),
    ('test', 3, 1, -50.0, -50.0, -50.0),
    ('test2', 0, 0, 0.0, 0.0, 0.0),
    ('test', 5, 2, 100.0, 0.0, 0.0);