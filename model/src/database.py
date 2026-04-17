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

def fetch_recent_ble_data(cursor, window_start, window_end):
    """
    指定した時間窓（60秒など）のBLE生データを取得する
    戻り値: 辞書型のリスト (例: [{'timestamp': ..., 'sensor_id': ..., 'other_data': ...}, ...])
    """
    query = """
        SELECT timestamp, sensor_id, other_data 
        FROM ble_data 
        WHERE timestamp >= %s AND timestamp < %s
    """
    cursor.execute(query, (window_start, window_end))
    return cursor.fetchall()

def save_prediction(connection, cursor, window_start, window_end, wait_time_min):
    """
    推論結果（待ち時間）をpredictionsテーブルに保存する
    """
    query = """
        INSERT INTO predictions 
        (window_start, window_end, prediction_waittime_min, predicted_at, model_version)
        VALUES (%s, %s, %s, %s, %s)
    """
    predicted_at = datetime.now()
    
    try:
        cursor.execute(query, (window_start, window_end, wait_time_min, predicted_at, MODEL_VERSION))
        connection.commit()  # 変更を確定させる
        print(f"[{predicted_at.strftime('%H:%M:%S')}] 予測完了: {wait_time_min:.1f}分 (対象: {window_start.strftime('%H:%M:%S')} ~ {window_end.strftime('%H:%M:%S')})")
    except mysql.connector.Error as err:
        print(f"予測結果の保存に失敗しました: {err}")
        connection.rollback()  # エラーが起きたら元に戻す