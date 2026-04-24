from flask import Flask, jsonify
import mysql.connector
from datetime import datetime
from typing import Dict, Any, Tuple

app = Flask(__name__)

# MySQLに接続してコネクションを返す関数
def get_db_connection():
    print("[DB] MySQLへの接続を試みる...")
    conn = mysql.connector.connect(
        host="mysql",        # docker-compose.ymlのサービス名
        user="project-e",
        password="project-e",
        database="ble_db"
    )
    print("[DB] 接続成功")
    return conn

# Frontendから「予測結果をください」というリクエストを受け取るエンドポイント
@app.route("/prediction", methods=["GET"])
def prediction() -> Tuple[Dict[str, Any], int]:
    print("[prediction] リクエストを受け取りました")
    
    # try/except で、エラーが起きてもプログラムが止まらないようにする
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        print("[prediction] カーソル取得完了")
        
        # predict_resultsテーブルから最新1件のデータを取得するSQLクエリ
        # ORDER BY created_at DESC で時刻が新しい順に並べ替え
        # LIMIT 1 で上から1行だけ取得
        sql = """
            SELECT created_at, predicted_value
            FROM predict_results
            ORDER BY created_at DESC
            LIMIT 1
        """

        cursor.execute(sql)
        result = cursor.fetchone()
        print(f"[prediction] 取得完了: {result}")
        
        # 予測データが取得できたか確認
        if result:
            
            # 取得したデータをFrontendに返す
            response_data: Dict[str, Any] = {
                "prediction": int(result['predicted_value']),
                "timestamp": str(result['created_at'].isoformat())
            }
            print(f"[prediction] レスポンス返却: {response_data}")
            return jsonify(response_data), 200
        else:
            # データが存在しない場合はエラーメッセージを返す
            return jsonify({"error": "No prediction data found"}), 404
    
    # エラーが起きた場合の処理
    except mysql.connector.Error as e:
        print(f"[prediction] DBエラー: {e}")
        return jsonify({"error": "Database error", "detail": str(e)}), 500
    
    except Exception as e:
        print(f"[prediction] 予期せぬエラー: {e}")
        return jsonify({"error": "Unexpected error", "detail": str(e)}), 500
    
    # 成功・失敗どちらの場合も必ず実行される
    finally:
        cursor.close()
        conn.close()
        print("[prediction] DB接続を閉じました")
    
if __name__ == '__main__':
    app.use_reloader = False
    app.run(debug=True)






