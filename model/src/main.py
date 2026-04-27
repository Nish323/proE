# src/main.py

import time
from datetime import datetime
import mysql.connector

# window_start/endを使わなくなったので、timedelta や WINDOW_SECONDS のインポートは削除しました
from database import get_db_connection, fetch_latest_ble_data, save_prediction
from weather import get_current_weather
from features import calculate_all_features
from predictor import WaitTimePredictor

def run_inference_cycle(predictor):
    """
    1回分の推論サイクル（取得・計算・予測・保存）を実行する
    """
    connection = None
    cursor = None
    
    try:
        now = datetime.now()
        
        # 1. DB接続
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # 2. BLE生データの取得（最新3件を取得）
        ble_records = fetch_latest_ble_data(cursor, limit=3)
        
        # 3. 天気情報の取得
        weather_info = get_current_weather()
        
        if ble_records:
            # 4. 110次元の特徴量を計算
            features_dict = calculate_all_features(ble_records, weather_info, now)
            
            # 5. 推論実行
            predicted_time = predictor.predict(features_dict)
            
            # 6. 予測結果をDBに保存（windowの時間は渡さない）
            save_prediction(connection, cursor, predicted_time)
        else:
            print(f"[{now.strftime('%H:%M:%S')}] DBにBLEデータがありません。スキップします。")

    except mysql.connector.Error as err:
        print(f"データベースエラー: {err}")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        
    finally:
        # リソースを確実に解放する
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def main():
    print("========================================")
    print("   待ち時間推論サービス 起動 (v1.0)   ")
    print("========================================")
    
    # 推論エージェントの初期化
    predictor = WaitTimePredictor()
    
    while True:
        run_inference_cycle(predictor)
        
        # 次のサイクルまで待機 (1分間隔)
        time.sleep(60)

if __name__ == "__main__":
    main()