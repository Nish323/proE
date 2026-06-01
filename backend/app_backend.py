from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import json
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
# ラズパイからBLEデータを受け取るエンドポイント
# POST /insert
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

        # JSON化
        other_data = {
            "filename": file.filename,
            "content": text_data
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

        return jsonify({
            "message": "TXT uploaded successfully"
        }), 201

    except Exception as e:
        print(e)

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
                "prediction": result['prediction_waittime_min'],
                "timestamp": str(result['predicted_at'].isoformat()),
                "weather": result['weather']
            }
            return jsonify(response_data), 200
        else:
            return jsonify({"error": "No prediction data found"}), 404

    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "detail": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error", "detail": str(e)}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


if __name__ == '__main__':
    app.use_reloader = False
    app.run(debug=True)
