from flask import Flask, jsonify, request
import mysql.connector
import os
import json

app = Flask(__name__)

# ファイルパス
BUFFER_FILE = "/app/shared/Buffer.json"

# バッファの内容を返すAPIエンドポイント
# http://127.0.0.1:5001/prediction

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
    print(f"[insert] 受け取ったデータ: {data}")

    # JSONから各フィールドを取り出す
    sensor_id         = data["sensor_id"]
    sequence_no       = data["sequence_no"]
    scan_duration_sec = data["scan_duration_sec"]
    scanned_at_str    = data["scanned_at"]
    observations      = data["observations"]

@app.route('/prediction', methods=['GET'])
def get_prediction():
    if not os.path.exists(BUFFER_FILE):
        return jsonify({"error": "Buffer file not found"}), 404

    with open(BUFFER_FILE, 'r') as f:
        data = json.load(f)

    if not data:
        return jsonify({"error": "No data available"}), 404

    # 最新のデータを返す
    latest_data = data[-1]
    return jsonify(latest_data)

if __name__ == '__main__':
    app.run(debug=True)