# src/predictor.py

import os
from catboost import CatBoostRegressor
from config import MODEL_PATH
from features import get_ordered_feature_list

class WaitTimePredictor:
    def __init__(self):
        self.model = CatBoostRegressor()
        self.is_loaded = False
        self._load_model()

    def _load_model(self):
        """モデルファイルを読み込む"""
        if os.path.exists(MODEL_PATH):
            try:
                self.model.load_model(str(MODEL_PATH))
                self.is_loaded = True
                print(f"モデルを読み込みました: {MODEL_PATH}")
            except Exception as e:
                print(f"モデルの読み込みに失敗しました: {e}")
        else:
            print(f"警告: モデルファイルが見つかりません: {MODEL_PATH}")
            print("ダミーモードで動作します（予測値として常に15.5を返します）")

    def predict(self, features_dict):
        """
        辞書形式の特徴量を受け取り、CatBoostで推論を行う
        """
        if not self.is_loaded:
            # モデルがない場合はテスト用に固定値を返す
            return 15.5

        # 1. 辞書をCatBoostが求める110次元の「正しい順番のリスト」に変換
        feature_list = get_ordered_feature_list(features_dict)

        # 2. 推論実行 (CatBoostは2次元配列を期待するので [[...]] にする)
        prediction = self.model.predict([feature_list])[0]

        # 予測値がマイナスにならないよう調整（機械学習の性質上稀にあるため）
        return max(0.0, float(prediction))