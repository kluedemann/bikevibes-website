DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS accelerometer;

CREATE TABLE locations (
    user_id TEXT NOT NULL,
    time_stamp INTEGER NOT NULL,
    trip_id INTEGER,
    latitude REAL,
    longitude REAL,
    PRIMARY KEY (user_id, time_stamp)
);

CREATE TABLE accelerometer (
    user_id TEXT NOT NULL,
    time_stamp INTEGER NOT NULL,
    trip_id INTEGER,
    x_accel REAL,
    y_accel REAL,
    z_accel REAL,
    PRIMARY KEY (user_id, time_stamp)
);
