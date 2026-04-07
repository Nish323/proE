import React from "react";
// import logo from "./logo.svg";
import "./App.css";
import axios, { AxiosError } from "axios"; // AxiosErrorをインポート
import { useEffect, useState } from "react";
import { Navbar } from "./components/Navbar/Navbar";
import { Box } from "./components/Box/Box";

type PredictionData = {
  prediction: string;
  timestamp: string;
};

function App() {
  const [data, setData] = useState<PredictionData>({
    prediction: "",
    timestamp: "",
  });
  const [error, setError] = useState<string | null>(null);
  const [refresh, setRefresh] = useState<boolean>(false);

  const fetchData = () => {
    axios
      .get<PredictionData>("http://localhost:5001/prediction")
      .then((res) => {
        setData(res.data);
        setError(null);
      })
      .catch((err: AxiosError) => {
        // errの型をAxiosErrorに指定
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

  return (
    <>
      <Navbar onRefreshClick={handleRefreshClick} />
      <div className="App">
        <h1>予測データ</h1>
        {error ? (
          <p style={{ color: "red" }}>{error}</p>
        ) : data.prediction ? ( // data自体ではなく、data.predictionの存在をチェック
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
        <div className="box-container">
          <Box value={55} unit="%" label="ただいまの混雑度" />
          <Box value={120} unit="人" label="ただいまの人数" />
          <Box value="晴れ" label="ただいまの天気" />
          <Box value="10:30" label="ただいまの時刻" />
        </div>
      </div>
    </>
  );
}

export default App;
