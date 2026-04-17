# src/test_local.py
# テストデータ作成用なので見なくても大丈夫です。

import json
from datetime import datetime
from weather import get_current_weather
from features import calculate_all_features
from predictor import WaitTimePredictor

print("========================================")
print(" 🚀 モデル単体テスト（DB連携なし）開始")
print("========================================")

# 1. 偽物（モック）のDBデータを作成する
# 実際にRaspberry Piから送られてくるのと同じ形のデータを用意します
dummy_db_records = [
    {
        'timestamp': datetime.now(),
        'sensor_id': 'raspi01',
        'other_data': json.dumps({
            "observations": [
                {"mac_address": "AA:BB:CC:11:22:33", "rssi": -55},
                {"mac_address": "DD:EE:FF:44:55:66", "rssi": -85}
            ]
        })
    },
    {
        'timestamp': datetime.now(),
        'sensor_id': 'raspi02',
        'other_data': json.dumps({
            "observations": [
                {"mac_address": "AA:BB:CC:11:22:33", "rssi": -70}
            ]
        })
    }
]

try:
    # 2. 天気APIのテスト
    print("\n[1/3] 天気API (weather.py) のテスト中...")
    weather_info = get_current_weather()
    print(f"  👉 取得成功: {weather_info}")

    # 3. 特徴量計算のテスト（一番重要！）
    print("\n[2/3] 特徴量計算 (features.py) のテスト中...")
    now = datetime.now()
    features = calculate_all_features(dummy_db_records, weather_info, now)
    
    print(f"  👉 計算完了: 生成された特徴量は {len(features)} 次元です。")

    # ==========================================
    # 🔍 ここから追加：110次元の中身を出力して確認する
    # ==========================================
    import pprint
    
    print("\n--- 📊 特徴量（辞書形式）の中身 ---")
    # sort_dicts=False にすることで、計算した順番通りに表示されます
    pprint.pprint(features, sort_dicts=False)

    # もし「CatBoostに渡す直前のただの数字の羅列（リスト）」も見たい場合はこちらも追加
    from features import get_ordered_feature_list
    feature_list = get_ordered_feature_list(features)
    print("\n--- 🤖 モデルに入力される最終リスト (長さ: {}) ---".format(len(feature_list)))
    print(feature_list)
    # ==========================================

    if len(features) == 110:
        print("\n  🟢 大成功！想定通りの110次元の特徴量が生成されました！")
    # 4. 推論のテスト
    print("\n[3/3] 推論モデル (predictor.py) のテスト中...")
    predictor = WaitTimePredictor()
    predicted_time = predictor.predict(features)
    print(f"  👉 推論成功: 予測待ち時間は {predicted_time:.1f} 分です！")

    print("\n========================================")
    print(" 🎉 すべての単体テストをクリアしました！")
    print("========================================")

except Exception as e:
    print(f"\n❌ エラー発生: {e}")