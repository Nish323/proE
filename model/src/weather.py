# src/weather.py

import requests

# config.py から緯度・経度の設定値を読み込む
from config import LOCATION_LAT, LOCATION_LON

def get_current_weather():
    """
    Open-Meteoから現在の天気(WMOコード)と気温を取得し、
    モデルに入力するための特徴量辞書に変換して返す
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LOCATION_LAT}&longitude={LOCATION_LON}&current=temperature_2m,weather_code&timezone=Asia%2FTokyo"
    
    try:
        # タイムアウト(5秒)を設定して通信が固まるのを防ぐ
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # HTTPエラーがあれば例外を発生させる
        data = response.json()
        
        temperature = data['current']['temperature_2m']
        wmo_code = data['current']['weather_code']
        
        # WMOコードを独自カテゴリ(0:晴れ, 1:曇り, 2:その他)に変換
        # 0: 快晴, 1: 晴れ, 2: 一部曇, 3: 曇り
        if wmo_code in [0, 1]:
            weather_category = 0  # 晴れ
        elif wmo_code in [2, 3]:
            weather_category = 1  # 曇り
        else:
            weather_category = 2  # その他（雨、雪、霧など）
            
        return {
            'temperature': temperature,
            'weather_category': weather_category,
            'weather_sunny': 1 if weather_category == 0 else 0,
            'weather_cloudy': 1 if weather_category == 1 else 0,
            'weather_other': 1 if weather_category == 2 else 0
        }
        
    except Exception as e:
        print(f"天気取得エラー: {e}")
        # APIが落ちていても推論システム全体を止めないよう、デフォルト値を返す
        return {
            'temperature': 20.0, 
            'weather_category': -1, 
            'weather_sunny': 0, 
            'weather_cloudy': 0, 
            'weather_other': 0
        }