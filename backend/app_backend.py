from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import json
import re
from datetime import datetime
from typing import Dict, Any, Tuple

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})


# -----------------------------------------------
# MySQLに接続してコネクションを返す関数
# -----------------------------------------------
def get_db_connection():
    print("[DB] MySQLへの接続を試みる...")
    conn = mysql.connector.connect(
        host="mysql",
        user="project-e",
        password="project-e",
        database="ble_db"
    )
    print("[DB] 接続成功")
    return conn


# -----------------------------------------------
# ラズパイのTXTから observations を作る関数
# -----------------------------------------------
def parse_ble_txt(content):
    observations = []

    pattern = r"Device:\s+(.+?)\s+-\s+rssi:\s+(-?\d+)"

    for match in re.finditer(pattern, content):
        device_name = match.group(1).strip()
        rssi = int(match.group(2))

        observations.append({
            "mac_address": device_name,
            "rssi": rssi
        })

    return observations


# -----------------------------------------------
# ラズパイからBLEデータを受け取るエンドポイント
# POST /upload_txt
# -----------------------------------------------
@app.route("/upload_txt", methods=["POST"])
def upload_txt():
    print("[upload_txt] リクエストを受け取りました")

    conn = None
    cursor = None

    try:
        # multipart/form-dataから取得
        file = request.files["file"]
        sensor_id = request.form["device_id"]

        # txt内容を文字列として取得
        text_data = file.read().decode("utf-8")

        print(f"sensor_id={sensor_id}")
        print(text_data)

        # txt内容から observations を作成
        observations = parse_ble_txt(text_data)

        print(f"[upload_txt] observations count = {len(observations)}")

        # JSON化
        other_data = {
            "filename": file.filename,
            "content": text_data,
            "observations": observations
        }

        # Scan Time を抽出
        timestamp = datetime.now()

        for line in text_data.splitlines():
            if line.startswith("Scan Time:"):
                timestamp_str = line.replace("Scan Time:", "").strip()

                timestamp = datetime.strptime(
                    timestamp_str,
                    "%Y-%m-%d %H:%M:%S"
                )
                break

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO ble_data
        (timestamp, sensor_id, other_data)
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                timestamp,
                sensor_id,
                json.dumps(other_data, ensure_ascii=False)
            )
        )

        conn.commit()

        print("[upload_txt] INSERT完了")

        return jsonify({
            "message": "TXT uploaded successfully",
            "sensor_id": sensor_id,
            "observations_count": len(observations)
        }), 201

    except Exception as e:
        print("[upload_txt] ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


# -----------------------------------------------
# フロントエンドへ予測結果を返すエンドポイント
# GET /prediction
# -----------------------------------------------
@app.route("/prediction", methods=["GET"])
def prediction() -> Tuple[Dict[str, Any], int]:
    print("[prediction] リクエストを受け取りました")

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT prediction_waittime_min, predicted_at, weather
            FROM predictions
            ORDER BY predicted_at DESC
            LIMIT 1
        """

        cursor.execute(sql)
        result = cursor.fetchone()

        if result:
            response_data: Dict[str, Any] = {
                "prediction": result["prediction_waittime_min"],
                "timestamp": str(result["predicted_at"].isoformat()),
                "weather": result["weather"]
            }
            return jsonify(response_data), 200
        else:
            return jsonify({"error": "No prediction data found"}), 404

    except mysql.connector.Error as e:
        return jsonify({
            "error": "Database error",
            "detail": str(e)
        }), 500

    except Exception as e:
        return jsonify({
            "error": "Unexpected error",
            "detail": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


if __name__ == "__main__":
    app.use_reloader = False
    app.run(debug=True)