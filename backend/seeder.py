"""
seeder.py  —  ble_data & predictions テーブルへのダミーデータ投入スクリプト

使い方（Docker起動後にホストから実行）:
    pip install mysql-connector-python
    python seeder.py

または Docker コンテナ内から:
    docker exec -it <backendコンテナ名> python seeder.py
"""

import mysql.connector
import json
import random
import string
from datetime import datetime, timedelta

# ========================================
# 接続設定（docker-compose.yml に合わせる）
# ========================================
DB_CONFIG = {
    "host":     "mysql",   # 変更: "127.0.0.1" → "mysql"
    "port":     3306,      # 変更: 3307 → 3306
    "user":     "project-e",
    "password": "project-e",
    "database": "ble_db",
}

# ========================================
# シーダー設定
# ========================================
RASPI_DEVICES  = ["raspi01", "raspi02", "raspi03", "raspi04", "raspi05"]
BLE_ROWS       = 30   # ble_data に投入する件数
PREDICTION_ROWS = 5   # predictions に投入する件数
MODEL_VERSION  = "catboost_v1.0"


# ----------------------------------------
# ユーティリティ
# ----------------------------------------
def random_mac() -> str:
    """ランダムな MAC アドレスを生成する"""
    return ":".join(
        "".join(random.choices("0123456789ABCDEF", k=2)) for _ in range(6)
    )

def random_observations(count: int = None) -> list:
    """observations リストを生成する（MACアドレス + RSSI）"""
    n = count or random.randint(3, 15)
    return [
        {
            "mac_address": random_mac(),
            "rssi": random.randint(-100, -40),
        }
        for _ in range(n)
    ]

def make_other_data(sensor_id: str, sequence_no: int, scanned_at: str) -> dict:
    """Raspberry Pi が送ってくる JSON と同じ構造のダミーを作る"""
    return {
        "schema_version": "1.0",
        "sensor_id":      sensor_id,
        "scanned_at":     scanned_at,
        "scan_duration_sec": random.randint(10, 60),
        "sequence_no":    sequence_no,
        "observations":   random_observations(),
    }


# ----------------------------------------
# ble_data シーダー
# ----------------------------------------
def seed_ble_data(cursor, conn):
    print(f"\n[ble_data] {BLE_ROWS} 件のダミーデータを投入します...")

    base_time = datetime.now() - timedelta(minutes=BLE_ROWS)
    seq_counter = {d: 1 for d in RASPI_DEVICES}
    inserted = 0

    for i in range(BLE_ROWS):
        sensor_id   = random.choice(RASPI_DEVICES)
        sequence_no = seq_counter[sensor_id]
        seq_counter[sensor_id] += 1

        # 1分ごとに少しずつ時刻をずらす
        timestamp   = base_time + timedelta(minutes=i, seconds=random.randint(0, 30))
        scanned_at  = timestamp.isoformat()
        other_data  = make_other_data(sensor_id, sequence_no, scanned_at)

        sql = """
            INSERT IGNORE INTO ble_data
                (timestamp, sensor_id, sequence_no, other_data)
            VALUES (%s, %s, %s, %s)
        """
        try:
            cursor.execute(sql, (
                timestamp,
                sensor_id,
                sequence_no,
                json.dumps(other_data),
            ))
            inserted += 1
        except mysql.connector.Error as e:
            print(f"  SKIP (重複など): sensor={sensor_id} seq={sequence_no} → {e}")

    conn.commit()
    print(f"[ble_data] 完了: {inserted} 件挿入しました")


# ----------------------------------------
# predictions シーダー
# ----------------------------------------
def seed_predictions(cursor, conn):
    print(f"\n[predictions] {PREDICTION_ROWS} 件のダミーデータを投入します...")

    base_time = datetime.now() - timedelta(minutes=PREDICTION_ROWS)
    inserted  = 0

    for i in range(PREDICTION_ROWS):
        predicted_at           = base_time + timedelta(minutes=i)
        prediction_waittime_min = round(random.uniform(1.0, 30.0), 2)

        sql = """
            INSERT INTO predictions
                (prediction_waittime_min, predicted_at, model_version)
            VALUES (%s, %s, %s)
        """
        try:
            cursor.execute(sql, (
                prediction_waittime_min,
                predicted_at,
                MODEL_VERSION,
            ))
            inserted += 1
            print(f"  → 予測待ち時間: {prediction_waittime_min:.1f} 分 ({predicted_at.strftime('%H:%M:%S')})")
        except mysql.connector.Error as e:
            print(f"  ERROR: {e}")

    conn.commit()
    print(f"[predictions] 完了: {inserted} 件挿入しました")


# ----------------------------------------
# メイン
# ----------------------------------------
def main():
    print("=" * 40)
    print("  シーダー起動")
    print("=" * 40)

    try:
        conn   = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("[DB] 接続成功")

        seed_ble_data(cursor, conn)
        seed_predictions(cursor, conn)

        print("\n[完了] すべてのダミーデータを投入しました")

    except mysql.connector.Error as e:
        print(f"\n[ERROR] DB接続またはクエリに失敗しました: {e}")
        print("docker-compose up でDBが起動しているか確認してください")

    finally:
        if "cursor" in dir():
            cursor.close()
        if "conn" in dir() and conn.is_connected():
            conn.close()
            print("[DB] 接続を閉じました")


if __name__ == "__main__":
    main()
