from flask import Flask, jsonify, request
import mysql.connector
import json

# 文字列をdatetime型に変換するために使う
from datetime import datetime

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

# ラズパイからBLEデータを受け取るエンドポイント
@app.route("/insert", methods=["POST"])
def insert():
    print("[insert] リクエストを受け取りました")

    # リクエストのJSONを取り出す
    data = request.get_json()

    # ↓ 追加: JSONが読み取れなかった場合のチェック
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400

    print(f"[insert] 受け取ったデータ: {data}")

    # ↓ 追加: 必須フィールドが全て揃っているかチェック
    required_fields = ["sensor_id", "sequence_no", "scanned_at", "observations"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # 各フィールドを明示的に型変換して取り出す
    sensor_id   = str(data["sensor_id"])
    sequence_no = int(data["sequence_no"])

    # ISO 8601形式の文字列をdatetime型に変換する（例: "2025-01-01T12:00:00+09:00"）
    # ↓ 追加: 変換失敗した場合のチェック
    try:
        timestamp = datetime.fromisoformat(data["scanned_at"])
    except ValueError:
        return jsonify({"error": f"Invalid scanned_at format: {data['scanned_at']}"}), 400

    # JSON全文をそのまま文字列化してDBに入れる（scan_duration_secも含まれる）
    other_data_json = json.dumps(data)

    # ↓ 追加: DB操作全体をtry/except/finallyで囲む
    try:
        conn   = get_db_connection()
        cursor = conn.cursor()
        print("[insert] カーソル取得完了")

        # カラム名をDBのスキーマに合わせたINSERT文（%sはSQL用のプレースホルダ）
        sql = """
            INSERT INTO ble_data (timestamp, sensor_id, sequence_no, other_data)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (timestamp, sensor_id, sequence_no, other_data_json))
        print("[insert] INSERT実行完了")

        # コミットしないとDBに反映されないので必ず呼ぶ
        conn.commit()
        print("[insert] コミット完了")

    # ↓ 追加: DBエラーが起きた場合にクラッシュせずエラーメッセージを返す
    except mysql.connector.Error as e:
        print(f"[insert] DBエラー: {e}")
        return jsonify({"error": "Database error", "detail": str(e)}), 500

    # ↓ 追加: 成功・失敗どちらの場合も必ずDB接続を閉じる
    finally:
        cursor.close()
        conn.close()

    # 論文のAPI2レスポンス例に合わせた形で返す
    # return jsonify({"message": "Data inserted successfully"}), 200

if __name__ == '__main__':
    app.use_reloader = False
    app.run(debug=True)
