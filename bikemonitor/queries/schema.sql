DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS accelerometer;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS surfaces;

CREATE TABLE locations (
    user_id TEXT NOT NULL,
    time_stamp INTEGER NOT NULL,
    trip_id INTEGER,
    latitude REAL,
    longitude REAL,
    PRIMARY KEY (user_id, time_stamp),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE accelerometer (
    user_id TEXT NOT NULL,
    time_stamp INTEGER NOT NULL,
    trip_id INTEGER,
    x_accel REAL,
    y_accel REAL,
    z_accel REAL,
    PRIMARY KEY (user_id, time_stamp),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE users (
    user_id TEXT NOT NULL,
    alias TEXT UNIQUE,
    PRIMARY KEY (user_id)
);

CREATE TABLE surfaces (
    user_id TEXT NOT NULL,
    trip_id INTEGER NOT NULL,
    surface TEXT,
    PRIMARY KEY (user_id, trip_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
