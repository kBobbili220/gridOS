CREATE TABLE batteries (
    battery_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    capacity_kwh NUMERIC(8, 2) NOT NULL,
    location TEXT,
    max_charge_kw NUMERIC(8, 2) NOT NULL,
    max_discharge_kw NUMERIC(8, 2) NOT NULL,
    min_soc_percent NUMERIC (5, 2) NOT NULL DEFAULT 20,

    CHECK (capacity_kwh > 0),
    CHECK (max_charge_kw > 0),
    CHECK (max_discharge_kw > 0),
    CHECK (min_soc_percent BETWEEN 0 AND 100)
);

CREATE TABLE telemetry (
    battery_id INTEGER NOT NULL, 
    recorded_at TIMESTAMPTZ NOT NULL, 
    power_kw NUMERIC(8, 3) NOT NULL, 
    temperature_c NUMERIC(5, 2) NOT NULL, 
    soc_percent NUMERIC (5, 2) NOT NULL,

    PRIMARY KEY (battery_id, recorded_at),
    FOREIGN KEY (battery_id) REFERENCES batteries(battery_id),

    CHECK (soc_percent BETWEEN 0 AND 100)
);