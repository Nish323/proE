-- ========================================
-- seeder.sql  ダミーデータ投入スクリプト
-- 使い方:
--   mysql/mysql-init/ フォルダに置くだけで
--   docker-compose up 時に自動実行されます
-- ========================================

USE ble_db;

-- ----------------------------------------
-- ble_data ダミーデータ（30件）
-- ----------------------------------------
INSERT IGNORE INTO ble_data (timestamp, sensor_id, other_data) VALUES
('2026-05-26 11:00:00.000', 'raspi01', '{"schema_version":"1.0","sensor_id":"raspi01","scanned_at":"2026-05-26T11:00:00","scan_duration_sec":30,"sequence_no":1,"observations":[{"mac_address":"AA:BB:CC:11:22:33","rssi":-55},{"mac_address":"DD:EE:FF:44:55:66","rssi":-72},{"mac_address":"11:22:33:AA:BB:CC","rssi":-88}]}'),
('2026-05-26 11:01:00.000', 'raspi02', '{"schema_version":"1.0","sensor_id":"raspi02","scanned_at":"2026-05-26T11:01:00","scan_duration_sec":30,"sequence_no":1,"observations":[{"mac_address":"AA:BB:CC:11:22:33","rssi":-60},{"mac_address":"FF:EE:DD:33:22:11","rssi":-75}]}'),
('2026-05-26 11:02:00.000', 'raspi03', '{"schema_version":"1.0","sensor_id":"raspi03","scanned_at":"2026-05-26T11:02:00","scan_duration_sec":30,"sequence_no":1,"observations":[{"mac_address":"BB:CC:DD:22:33:44","rssi":-65},{"mac_address":"CC:DD:EE:33:44:55","rssi":-80}]}'),
('2026-05-26 11:03:00.000', 'raspi04', '{"schema_version":"1.0","sensor_id":"raspi04","scanned_at":"2026-05-26T11:03:00","scan_duration_sec":30,"sequence_no":1,"observations":[{"mac_address":"AA:BB:CC:11:22:33","rssi":-70},{"mac_address":"11:22:33:AA:BB:CC","rssi":-85},{"mac_address":"22:33:44:BB:CC:DD","rssi":-92}]}'),
('2026-05-26 11:04:00.000', 'raspi05', '{"schema_version":"1.0","sensor_id":"raspi05","scanned_at":"2026-05-26T11:04:00","scan_duration_sec":30,"sequence_no":1,"observations":[{"mac_address":"DD:EE:FF:44:55:66","rssi":-58},{"mac_address":"EE:FF:00:55:66:77","rssi":-77}]}'),
('2026-05-26 11:05:00.000', 'raspi01', '{"schema_version":"1.0","sensor_id":"raspi01","scanned_at":"2026-05-26T11:05:00","scan_duration_sec":30,"sequence_no":2,"observations":[{"mac_address":"AA:BB:CC:11:22:33","rssi":-53},{"mac_address":"FF:EE:DD:33:22:11","rssi":-68},{"mac_address":"33:44:55:CC:DD:EE","rssi":-90}]}'),
('2026-05-26 11:06:00.000', 'raspi02', '{"schema_version":"1.0","sensor_id":"raspi02","scanned_at":"2026-05-26T11:06:00","scan_duration_sec":30,"sequence_no":2,"observations":[{"mac_address":"BB:CC:DD:22:33:44","rssi":-62},{"mac_address":"AA:BB:CC:11:22:33","rssi":-78}]}'),
('2026-05-26 11:07:00.000', 'raspi03', '{"schema_version":"1.0","sensor_id":"raspi03","scanned_at":"2026-05-26T11:07:00","scan_duration_sec":30,"sequence_no":2,"observations":[{"mac_address":"CC:DD:EE:33:44:55","rssi":-55},{"mac_address":"DD:EE:FF:44:55:66","rssi":-73},{"mac_address":"EE:FF:00:55:66:77","rssi":-95}]}'),
('2026-05-26 11:08:00.000', 'raspi04', '{"schema_version":"1.0","sensor_id":"raspi04","scanned_at":"2026-05-26T11:08:00","scan_duration_sec":30,"sequence_no":2,"observations":[{"mac_address":"AA:BB:CC:11:22:33","rssi":-67}]}'),
('2026-05-26 11:09:00.000', 'raspi05', '{"schema_version":"1.0","sensor_id":"raspi05","scanned_at":"2026-05-26T11:09:00","scan_duration_sec":30,"sequence_no":2,"observations":[{"mac_address":"11:22:33:AA:BB:CC","rssi":-59},{"mac_address":"22:33:44:BB:CC:DD","rssi":-76},{"mac_address":"33:44:55:CC:DD:EE","rssi":-88}]}'),
('2026-05-26 11:10:00.000', 'raspi01', '{"schema_version":"1.0","sensor_id":"raspi01","scanned_at":"2026-05-26T11:10:00","scan_duration_sec":30,"sequence_no":3,"observations":[{"mac_address":"AA:BB:CC:11:22:33","rssi":-50},{"mac_address":"BB:CC:DD:22:33:44","rssi":-65},{"mac_address":"FF:EE:DD:33:22:11","rssi":-82}]}'),
('2026-05-26 11:11:00.000', 'raspi02', '{"schema_version":"1.0","sensor_id":"raspi02","scanned_at":"2026-05-26T11:11:00","scan_duration_sec":30,"sequence_no":3,"observations":[{"mac_address":"DD:EE:FF:44:55:66","rssi":-71},{"mac_address":"EE:FF:00:55:66:77","rssi":-86}]}'),
('2026-05-26 11:12:00.000', 'raspi03', '{"schema_version":"1.0","sensor_id":"raspi03","scanned_at":"2026-05-26T11:12:00","scan_duration_sec":30,"sequence_no":3,"observations":[{"mac_address":"AA:BB:CC:11:22:33","rssi":-64},{"mac_address":"33:44:55:CC:DD:EE","rssi":-79}]}'),
('2026-05-26 11:13:00.000', 'raspi04', '{"schema_version":"1.0","sensor_id":"raspi04","scanned_at":"2026-05-26T11:13:00","scan_duration_sec":30,"sequence_no":3,"observations":[{"mac_address":"BB:CC:DD:22:33:44","rssi":-56},{"mac_address":"CC:DD:EE:33:44:55","rssi":-74},{"mac_address":"AA:BB:CC:11:22:33","rssi":-91}]}'),
('2026-05-26 11:14:00.000', 'raspi05', '{"schema_version":"1.0","sensor_id":"raspi05","scanned_at":"2026-05-26T11:14:00","scan_duration_sec":30,"sequence_no":3,"observations":[{"mac_address":"FF:EE:DD:33:22:11","rssi":-63},{"mac_address":"11:22:33:AA:BB:CC","rssi":-80}]}'),
('2026-05-26 11:15:00.000', 'raspi01', '{"schema_version":"1.0","sensor_id":"raspi01","scanned_at":"2026-05-26T11:15:00","scan_duration_sec":30,"sequence_no":4,"observations":[{"mac_address":"AA:BB:CC:11:22:33","rssi":-52},{"mac_address":"EE:FF:00:55:66:77","rssi":-69}]}'),
('2026-05-26 11:16:00.000', 'raspi02', '{"schema_version":"1.0","sensor_id":"raspi02","scanned_at":"2026-05-26T11:16:00","scan_duration_sec":30,"sequence_no":4,"observations":[{"mac_address":"22:33:44:BB:CC:DD","rssi":-77},{"mac_address":"33:44:55:CC:DD:EE","rssi":-93}]}'),
('2026-05-26 11:17:00.000', 'raspi03', '{"schema_version":"1.0","sensor_id":"raspi03","scanned_at":"2026-05-26T11:17:00","scan_duration_sec":30,"sequence_no":4,"observations":[{"mac_address":"DD:EE:FF:44:55:66","rssi":-61},{"mac_address":"AA:BB:CC:11:22:33","rssi":-76},{"mac_address":"BB:CC:DD:22:33:44","rssi":-89}]}'),
('2026-05-26 11:18:00.000', 'raspi04', '{"schema_version":"1.0","sensor_id":"raspi04","scanned_at":"2026-05-26T11:18:00","scan_duration_sec":30,"sequence_no":4,"observations":[{"mac_address":"FF:EE:DD:33:22:11","rssi":-57}]}'),
('2026-05-26 11:19:00.000', 'raspi05', '{"schema_version":"1.0","sensor_id":"raspi05","scanned_at":"2026-05-26T11:19:00","scan_duration_sec":30,"sequence_no":4,"observations":[{"mac_address":"CC:DD:EE:33:44:55","rssi":-66},{"mac_address":"EE:FF:00:55:66:77","rssi":-83}]}'),
('2026-05-26 11:20:00.000', 'raspi01', '{"schema_version":"1.0","sensor_id":"raspi01","scanned_at":"2026-05-26T11:20:00","scan_duration_sec":30,"sequence_no":5,"observations":[{"mac_address":"AA:BB:CC:11:22:33","rssi":-54},{"mac_address":"11:22:33:AA:BB:CC","rssi":-70},{"mac_address":"DD:EE:FF:44:55:66","rssi":-87}]}'),
('2026-05-26 11:21:00.000', 'raspi02', '{"schema_version":"1.0","sensor_id":"raspi02","scanned_at":"2026-05-26T11:21:00","scan_duration_sec":30,"sequence_no":5,"observations":[{"mac_address":"BB:CC:DD:22:33:44","rssi":-63},{"mac_address":"FF:EE:DD:33:22:11","rssi":-79}]}'),
('2026-05-26 11:22:00.000', 'raspi03', '{"schema_version":"1.0","sensor_id":"raspi03","scanned_at":"2026-05-26T11:22:00","scan_duration_sec":30,"sequence_no":5,"observations":[{"mac_address":"AA:BB:CC:11:22:33","rssi":-58},{"mac_address":"22:33:44:BB:CC:DD","rssi":-74}]}'),
('2026-05-26 11:23:00.000', 'raspi04', '{"schema_version":"1.0","sensor_id":"raspi04","scanned_at":"2026-05-26T11:23:00","scan_duration_sec":30,"sequence_no":5,"observations":[{"mac_address":"33:44:55:CC:DD:EE","rssi":-68},{"mac_address":"CC:DD:EE:33:44:55","rssi":-84},{"mac_address":"EE:FF:00:55:66:77","rssi":-96}]}'),
('2026-05-26 11:24:00.000', 'raspi05', '{"schema_version":"1.0","sensor_id":"raspi05","scanned_at":"2026-05-26T11:24:00","scan_duration_sec":30,"sequence_no":5,"observations":[{"mac_address":"AA:BB:CC:11:22:33","rssi":-51},{"mac_address":"DD:EE:FF:44:55:66","rssi":-67}]}'),
('2026-05-26 11:25:00.000', 'raspi01', '{"schema_version":"1.0","sensor_id":"raspi01","scanned_at":"2026-05-26T11:25:00","scan_duration_sec":30,"sequence_no":6,"observations":[{"mac_address":"FF:EE:DD:33:22:11","rssi":-60},{"mac_address":"11:22:33:AA:BB:CC","rssi":-75},{"mac_address":"BB:CC:DD:22:33:44","rssi":-90}]}'),
('2026-05-26 11:26:00.000', 'raspi02', '{"schema_version":"1.0","sensor_id":"raspi02","scanned_at":"2026-05-26T11:26:00","scan_duration_sec":30,"sequence_no":6,"observations":[{"mac_address":"CC:DD:EE:33:44:55","rssi":-64},{"mac_address":"AA:BB:CC:11:22:33","rssi":-81}]}'),
('2026-05-26 11:27:00.000', 'raspi03', '{"schema_version":"1.0","sensor_id":"raspi03","scanned_at":"2026-05-26T11:27:00","scan_duration_sec":30,"sequence_no":6,"observations":[{"mac_address":"22:33:44:BB:CC:DD","rssi":-73},{"mac_address":"EE:FF:00:55:66:77","rssi":-88}]}'),
('2026-05-26 11:28:00.000', 'raspi04', '{"schema_version":"1.0","sensor_id":"raspi04","scanned_at":"2026-05-26T11:28:00","scan_duration_sec":30,"sequence_no":6,"observations":[{"mac_address":"DD:EE:FF:44:55:66","rssi":-56},{"mac_address":"33:44:55:CC:DD:EE","rssi":-72}]}'),
('2026-05-26 11:29:00.000', 'raspi05', '{"schema_version":"1.0","sensor_id":"raspi05","scanned_at":"2026-05-26T11:29:00","scan_duration_sec":30,"sequence_no":6,"observations":[{"mac_address":"AA:BB:CC:11:22:33","rssi":-62},{"mac_address":"BB:CC:DD:22:33:44","rssi":-78},{"mac_address":"FF:EE:DD:33:22:11","rssi":-94}]}');

-- ----------------------------------------
-- predictions ダミーデータ（5件）
-- ----------------------------------------
INSERT INTO predictions (prediction_waittime_min, predicted_at, model_version) VALUES
(12.5, '2026-05-26 11:05:00.000', 'catboost_v1.0'),
(8.3,  '2026-05-26 11:10:00.000', 'catboost_v1.0'),
(15.7, '2026-05-26 11:15:00.000', 'catboost_v1.0'),
(6.2,  '2026-05-26 11:20:00.000', 'catboost_v1.0'),
(20.1, '2026-05-26 11:25:00.000', 'catboost_v1.0');
