from flask import Flask, jsonify, request
import mysql.connector
import json

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
    print(f"[insert] 受け取ったデータ: {data}")

    # JSONから各フィールドを取り出す
    sensor_id         = data["sensor_id"]
    sequence_no       = data["sequence_no"]
    scan_duration_sec = data["scan_duration_sec"]
    scanned_at_str    = data["scanned_at"]
    observations      = data["observations"]

    # 丸岡変更点: observationsはリスト形式なのでJSON文字列に変換してDBに入れられる形にする
    other_data_json = json.dumps(observations)
    print(f"[insert] other_data_json: {other_data_json}")

    # 丸岡変更点: DBに接続する
    conn   = get_db_connection()
    cursor = conn.cursor()
    print("[insert] カーソル取得完了")

    # 丸岡変更点: INSERT文を定義して実行する（%sはSQL用のプレースホルダ）
    sql = """
        INSERT INTO ble_data (sensor_id, sequence_no, scanned_at, scan_duration_sec, other_data)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (sensor_id, sequence_no, scanned_at_str, scan_duration_sec, other_data_json))
    print("[insert] INSERT実行完了")

    # 丸岡変更点: コミットしないとDBに反映されないので必ず呼ぶ
    conn.commit()
    print("[insert] コミット完了")

    # 丸岡変更点: リソースを解放する
    cursor.close()
    conn.close()

    # 丸岡変更点: 論文のAPI2レスポンス例に合わせた形で返す
    return jsonify({"message": "Data inserted successfully"}), 200


@app.route('/prediction', methods=['GET'])
def get_prediction():
    print("[prediction] リクエストを受け取りました")

    # 丸岡変更点: Buffer.jsonではなくDBから取得するように変更
    conn   = get_db_connection()
    cursor = conn.cursor()

    # 丸岡変更点: predictionsテーブルから最新3件を取得するSQL
    sql = """
        SELECT prediction_waittime_min, predicted_at
        FROM predictions
        ORDER BY predicted_at DESC
        LIMIT 3
    """
    cursor.execute(sql)
    print("[prediction] SELECT実行完了")

    # 丸岡変更点: 最新3件取得（最大3件、結果がなければ空リストになる）
    rows = cursor.fetchall()
    print(f"[prediction] 取得結果: {rows}")

    cursor.close()
    conn.close()

    # 丸岡変更点: データがなければ404を返す
    if not rows:
        return jsonify({"error": "No prediction available"}), 404

    # 丸岡変更点: 各行を辞書に変換してリストで返す
    result = [
        {"prediction": row[0], "timestamp": str(row[1])}
        for row in rows
    ]
    return jsonify(result), 200


if __name__ == '__main__':
    app.run(debug=True)
