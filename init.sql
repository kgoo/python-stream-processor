CREATE TABLE IF NOT EXISTS aggregates (
    value TEXT NOT NULL,
    window_start TIMESTAMP NOT NULL,
    count INTEGER,
    PRIMARY KEY (value, window_start)
);
