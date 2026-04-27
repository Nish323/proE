# src/config.py

import os
from pathlib import Path

# ========================================
# プロジェクト全体のパス設定
# ========================================
# このファイル(config.py)の親の親ディレクトリ(model)を基準にする
BASE_DIR = Path(__file__).resolve().parent.parent

# 学習済みCatBoostモデルの保存先
MODEL_PATH = BASE_DIR / "wait_time_model.cbm"
MODEL_VERSION = "catboost_v1.0"

# ========================================
# データベース(MySQL)接続設定
# ========================================
DB_CONFIG = {
    'host': 'mysql',          # docker-compose内のサービス名
    'user': 'project-e',
    'password': 'project-e',
    'database': 'ble_db',
    'port': 3306
}

# ========================================
# 天気API (Open-Meteo) 設定
# ========================================
# 愛媛県松山市の緯度・経度
LOCATION_LAT = 33.8392
LOCATION_LON = 132.7653

# ========================================
# 推論・特徴量計算に関する設定
# ========================================
# 予測に使用する時間窓（秒）
WINDOW_SECONDS = 60

# 予測対象となるRaspiデバイスのリスト
RASPI_DEVICES = [
    'raspi01', 
    'raspi02', 
    'raspi03', 
    'raspi04', 
    'raspi05'
]