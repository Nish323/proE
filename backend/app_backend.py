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

    data = request.get_data(as_text=True)
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400

    required_fields = ["sensor_id", "sequence_no", "scanned_at", "observations"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        sensor_id = int(data["sensor_id"])
    except (ValueError, TypeError):
        return jsonify({"error": f"Invalid sensor_id: {data['sensor_id']}"}), 400

    sequence_no = int(data["sequence_no"])

    try:
        timestamp = datetime.fromisoformat(data["scanned_at"])
    except ValueError:
        return jsonify({"error": f"Invalid scanned_at format: {data['scanned_at']}"}), 400

    other_data_json = json.dumps(data)

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO ble_data (timestamp, sensor_id, sequence_no, other_data)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (timestamp, sensor_id, sequence_no, other_data_json))
        conn.commit()
        return jsonify({"message": "Data inserted successfully"}), 201

    except mysql.connector.errors.IntegrityError:
        return jsonify({"error": "Duplicate entry"}), 409

    except mysql.connector.Error as e:
        return jsonify({"error": "Database error", "detail": str(e)}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


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
