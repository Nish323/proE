import React from "react";
import logo from "./logo.svg";
import "./App.css";
import axios, { AxiosError } from "axios"; // AxiosErrorをインポート
import { useEffect, useState } from "react";

type PredictionData = {
  prediction: string;
  timestamp: string;
};

function App() {
  const [data, setData] = useState<PredictionData>({ prediction: "", timestamp: "" });
  const [error, setError] = useState<string | null>(null);
  const [refresh, setRefresh] = useState<boolean>(false);

  const fetchData = () => {
    axios
      .get<PredictionData>("http://localhost:5001/prediction")
      .then((res) => {
        setData(res.data);
        setError(null);
      })
      .catch((err: AxiosError) => { // errの型をAxiosErrorに指定
        console.error("Error fetching data:", err);
        setError(`データの取得に失敗しました: ${err.message}`);
      });
  };

  useEffect(() => {
    fetchData();
  }, [refresh]);

  const handleRefreshClick = () => {
    setRefresh((prev) => !prev);
  };

  if (error) {
    return (
      <div className="App">
        <h1>予測データ</h1>
        <p style={{ color: "red" }}>{error}</p>
        <button onClick={handleRefreshClick}>更新</button>
      </div>
    );
  }

  return (
    <div className="App">
      <h1>予測データ</h1>
      {data.prediction ? ( // data自体ではなく、data.predictionの存在をチェック
        <div>
          <p>
            <strong>予測値:</strong> {data.prediction}
          </p>
          <p>
            <strong>タイムスタンプ:</strong> {data.timestamp}
          </p>
        </div>
      ) : (
        <p>データを読み込み中...</p>
      )}
      <button onClick={handleRefreshClick}>更新</button>
    </div>
  );
}

export default App;