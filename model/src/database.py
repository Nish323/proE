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
    最新のBLE生データを指定件数（デフォルト3件）取得する
    戻り値: 辞書型のリスト (例: [{'timestamp': ..., 'sensor_id': ..., 'other_data': ...}, ...])
    """
    # ORDER BY で時刻が新しい順に並べ替え、LIMIT で上から3件だけ取得する
    query = """
        SELECT timestamp, sensor_id, other_data 
        FROM ble_data 
        ORDER BY timestamp DESC
        LIMIT %s
    """
    cursor.execute(query, (limit,))
    return cursor.fetchall()

def save_prediction(connection, cursor, wait_time_min):
    """
    推論結果（待ち時間）をpredictionsテーブルに保存する
    """
    # window_start, window_end を削除し、残りの3項目だけを保存する
    query = """
        INSERT INTO predictions 
        (prediction_waittime_min, predicted_at, model_version)
        VALUES (%s, %s, %s)
    """
    predicted_at = datetime.now()
    
    try:
        cursor.execute(query, (wait_time_min, predicted_at, MODEL_VERSION))
        connection.commit()  # 変更を確定させる
        print(f"[{predicted_at.strftime('%H:%M:%S')}] 予測完了: {wait_time_min:.1f}分 (最新データに基づく推論)")
    except mysql.connector.Error as err:
        print(f"予測結果の保存に失敗しました: {err}")
        connection.rollback()  # エラーが起きたら元に戻す