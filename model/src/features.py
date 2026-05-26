# src/features.py

import math
import json
from datetime import datetime
from config import RASPI_DEVICES

# ========================================
# 授業情報（曜日別・時限別の対面授業数）
# 曜日: 0=月, 1=火, 2=水, 3=木, 4=金
# ========================================
CLASS_INFO = {
    2: {0: 190, 1: 177, 2: 198, 3: 152, 4: 143},  # 2限
    3: {0: 186, 1: 207, 2: 156, 3: 90, 4: 100},   # 3限
}

# ========================================
# 1. 時間・授業情報の特徴量計算
# ========================================
def get_period(dt):
    """時限を判定: 2限(11:00-12:30) or 3限(13:00-14:30)"""
    if 11 <= dt.hour < 13:
        return 2
    elif 13 <= dt.hour < 15:
        return 3
    return None

def calculate_time_and_class_features(target_time):
    """現在時刻から時間と授業に関する特徴量を計算"""
    features = {}
    
    # --- 時間特徴量 ---
    month = target_time.month
    features['month_sin'] = math.sin(2 * math.pi * month / 12)
    features['month_cos'] = math.cos(2 * math.pi * month / 12)
    
    # 11:30からの絶対時間差（秒）
    base_time = target_time.replace(hour=11, minute=30, second=0, microsecond=0)
    time_diff = (target_time - base_time).total_seconds()
    features['time_from_1130'] = max(0, time_diff)
    
    # 曜日（月=0 〜 金=4）のOne-Hotエンコーディング
    weekday = target_time.weekday()
    for i in range(5):
        features[f'weekday_{i}'] = 1 if weekday == i else 0
        
    # --- 授業情報特徴量 ---
    if weekday < 5:
        period = get_period(target_time)
        features['class_count'] = CLASS_INFO.get(period, {}).get(weekday, 0) if period else 0
        features['class_period_2'] = CLASS_INFO[2].get(weekday, 0)
        features['class_period_3'] = CLASS_INFO[3].get(weekday, 0)
    else:
        features['class_count'] = 0
        features['class_period_2'] = 0
        features['class_period_3'] = 0
        
    return features

# ========================================
# 2. BLE生データの解読とデバイス別特徴量計算
# ========================================
def calculate_single_device_features(observations, prefix):
    """1つのRaspiデバイスのMACアドレスリストから18個の特徴量を計算"""
    features = {}
    
    # 全MACアドレスとユニークMACアドレスを取得
    # JSONのキー名が 'mac' か 'mac_address' の両方に対応
    all_macs = [obs.get('mac_address', obs.get('mac', '')) for obs in observations]
    all_macs = [mac for mac in all_macs if mac] # 空文字を除外
    unique_macs = set(all_macs)
    
    # 基本特徴量（3個）
    features[f'{prefix}_total_count'] = len(all_macs)
    features[f'{prefix}_unique_count'] = len(unique_macs)
    features[f'{prefix}_unique_ratio'] = len(unique_macs) / len(all_macs) if all_macs else 0
    
    # RSSI閾値別特徴量（5閾値 x 3特徴 = 15個）
    thresholds = [-60, -70, -80, -90, -100]
    for threshold in thresholds:
        filtered = [obs for obs in observations if int(obs.get('rssi', -999)) >= threshold]
        filtered_macs = [obs.get('mac_address', obs.get('mac', '')) for obs in filtered]
        filtered_unique = set(filtered_macs)
        
        features[f'{prefix}_rssi{threshold}_total'] = len(filtered_macs)
        features[f'{prefix}_rssi{threshold}_unique'] = len(filtered_unique)
        features[f'{prefix}_rssi{threshold}_ratio'] = len(filtered_unique) / len(filtered_macs) if filtered_macs else 0
        
    return features

# ========================================
# 3. すべての特徴量を統合するメイン関数
# ========================================
def calculate_all_features(db_records, weather_info, target_time):
    """
    DBの生データと天気情報から、CatBoostに入力する110次元の特徴量辞書を作成する
    """
    features = {}
    
    # ① 時間・授業・天気特徴量の統合 (16個)
    features.update(calculate_time_and_class_features(target_time))
    features.update({
        'weather_category': weather_info['weather_category'],
        'temperature': weather_info['temperature'],
        'weather_sunny': weather_info['weather_sunny'],
        'weather_cloudy': weather_info['weather_cloudy'],
        'weather_other': weather_info['weather_other']
    })
    
    # ② DBレコードからJSONを解読し、デバイスごとにデータを振り分ける
    # 構造: {'raspi01': [{'mac': '...', 'rssi': -75}, ...], 'raspi02': [...]}
    device_observations = {device: [] for device in RASPI_DEVICES}
    
    for record in db_records:
        sensor_id = record['sensor_id']
        if sensor_id not in device_observations:
            continue
            
        try:
            # other_data は文字列として保存されている場合と、辞書型にパース済みの場合がある
            other_data = record['other_data']
            if isinstance(other_data, str):
                data_dict = json.loads(other_data)
            else:
                data_dict = other_data
                
            obs_list = data_dict.get('observations', [])
            device_observations[sensor_id].extend(obs_list)
        except Exception as e:
            print(f"JSONパースエラー ({sensor_id}): {e}")
            
    # ③ 各デバイスの特徴量を計算 (18個 x 5台 = 90個)
    all_devices_total_count = 0
    all_devices_unique_macs = set()
    active_devices_count = 0
    
    for device_name in RASPI_DEVICES:
        observations = device_observations[device_name]
        
        if len(observations) > 0:
            active_devices_count += 1
            all_devices_total_count += len(observations)
            macs = [obs.get('mac_address', obs.get('mac', '')) for obs in observations]
            all_devices_unique_macs.update(macs)
            
        # デバイスごとの18個の特徴量を計算して統合
        device_feats = calculate_single_device_features(observations, prefix=device_name)
        features.update(device_feats)
        
    # ④ 全デバイス統合特徴量 (4個)
    features['all_total_count'] = all_devices_total_count
    features['all_unique_count'] = len(all_devices_unique_macs)
    features['all_unique_ratio'] = len(all_devices_unique_macs) / all_devices_total_count if all_devices_total_count > 0 else 0
    features['num_devices'] = active_devices_count
    
    return features

# ========================================
# 4. CatBoost用の「正しい順番のリスト」を生成する関数
# ========================================
def get_ordered_feature_list(features_dict):
    """
    辞書型の特徴量を、CatBoostが学習した時と「全く同じ順番」のリストに変換する
    ※順番が1つでも狂うとAIが誤作動を起こすため超重要です！
    """
    ordered_keys = []
    
    # 1. 各raspiの特徴量 (18個 × 5台 = 90個)
    for device_name in RASPI_DEVICES:
        prefix = device_name
        ordered_keys.extend([
            f'{prefix}_total_count',
            f'{prefix}_unique_count',
            f'{prefix}_unique_ratio'
        ])
        for threshold in [-60, -70, -80, -90, -100]:
            ordered_keys.extend([
                f'{prefix}_rssi{threshold}_total',
                f'{prefix}_rssi{threshold}_unique',
                f'{prefix}_rssi{threshold}_ratio'
            ])
            
    # 2. 全デバイス統合特徴量 (4個)
    ordered_keys.extend([
        'all_total_count', 'all_unique_count', 'all_unique_ratio', 'num_devices'
    ])
    
    # 3. 時間・天気特徴量 (16個)
    ordered_keys.extend([
        'month_sin', 'month_cos', 'time_from_1130',
        'weekday_0', 'weekday_1', 'weekday_2', 'weekday_3', 'weekday_4',
        'class_period_2', 'class_period_3', 'class_count',
        'weather_category', 'temperature',
        'weather_sunny', 'weather_cloudy', 'weather_other'
    ])
    
    # 辞書からリストに変換して返す
    return [features_dict.get(key, 0) for key in ordered_keys]