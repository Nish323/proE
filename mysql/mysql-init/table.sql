-- ble_dataテーブル
CREATE TABLE IF NOT EXISTS ble_data (
    id          BIGINT      AUTO_INCREMENT PRIMARY KEY,
    timestamp   DATETIME(3) NOT NULL,
    sensor_id   VARCHAR(64) NOT NULL,
    sequence_no INT         NOT NULL,
    other_data  JSON        NOT NULL
);

CREATE UNIQUE INDEX uq_ble_data_sensor_seq
ON ble_data(sensor_id, sequence_no);

CREATE INDEX idx_ble_data_timestamp
ON ble_data(timestamp);

-- predictionsテーブル
CREATE TABLE IF NOT EXISTS predictions (
    id                      BIGINT      AUTO_INCREMENT PRIMARY KEY,
    window_start            DATETIME(3) NOT NULL,
    window_end              DATETIME(3) NOT NULL,
    prediction_waittime_min FLOAT       NOT NULL,
    predicted_at            DATETIME(3) NOT NULL,
    model_version           VARCHAR(64) NOT NULL
);

CREATE UNIQUE INDEX uq_predictions_window_model
ON predictions(window_start, window_end, model_version);

CREATE INDEX idx_predictions_predicted_at
ON predictions(predicted_at);