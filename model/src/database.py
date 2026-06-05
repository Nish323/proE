# src/database.py

import mysql.connector
from datetime import datetime

# config.py から設定値を読み込む
from config import DB_CONFIG, MODEL_VERSION

def get_db_connection():
    """データベースへの接続を作成して返す"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"DB接続エラー: {err}")
        raise

def fetch_latest_ble_data(cursor, limit=3):
    """
    sensor_idごとに最新limit件を取得する

    戻り値:
    [
        {
            'timestamp': ...,
            'sensor_id': 'raspi01',
            'other_data': ...
        },
        ...
    ]
    """

    query = """
        SELECT timestamp, sensor_id, other_data
        FROM (
            SELECT
                timestamp,
                sensor_id,
                other_data,
                ROW_NUMBER() OVER (
                    PARTITION BY sensor_id
                    ORDER BY timestamp DESC
                ) AS rn
            FROM ble_data
        ) ranked
        WHERE rn <= %s
        ORDER BY sensor_id, timestamp DESC
    """

    cursor.execute(query, (limit,))
    return cursor.fetchall()

def save_prediction(connection, cursor, wait_time_min, weather_category):
    """
    推論結果（待ち時間）と天気情報をpredictionsテーブルに保存する
    """
    # AIの数字(0,1,2)を、DB保存用の日本語の文字に変換
    weather_map = {0: "晴れ", 1: "曇り", 2: "雨・その他"}
    weather_text = weather_map.get(weather_category, "不明")

    # weatherカラムを追加
    query = """
        INSERT INTO predictions 
        (prediction_waittime_min, predicted_at, model_version, weather)
        VALUES (%s, %s, %s, %s)
    """
    predicted_at = datetime.now()
    
    try:
        # パラメータに weather_text を追加
        cursor.execute(query, (wait_time_min, predicted_at, MODEL_VERSION, weather_text))
        connection.commit()  # 変更を確定させる
        print(f"[{predicted_at.strftime('%H:%M:%S')}] 予測完了: {wait_time_min:.1f}分 (天気: {weather_text})")
    except mysql.connector.Error as err:
        print(f"予測結果の保存に失敗しました: {err}")
        connection.rollback()  # エラーが起きたら元に戻す
