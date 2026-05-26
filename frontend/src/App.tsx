import React from "react";
import "./App.css";
import axios, { AxiosError } from "axios";
import { useEffect, useState } from "react";
import { Navbar } from "./components/Navbar/Navbar";
import { Box } from "./components/Box/Box";
import { Footer } from "./components/Footer/Footer";
import { CurrentTime } from "./components/CurrentTime/CurrentTime";

type PredictionData = {
  prediction: number;
  timestamp: string;
  weather: string;
};

function App() {
  const [data, setData] = useState<PredictionData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [refresh, setRefresh] = useState<boolean>(false);
  const [lastFetchMessage, setLastFetchMessage] = useState<string>("");

  const fetchData = () => {
    axios
      .get<PredictionData>("http://localhost:5001/prediction")
      .then((res) => {
        setData(res.data);
        setError(null);
        setLastFetchMessage(`成功 (${new Date().toLocaleTimeString()})`);
      })
      .catch((err: AxiosError) => {
        console.error("Error fetching data:", err);
        setError(`データの取得に失敗しました: ${err.message}`);
        setLastFetchMessage(`失敗: ${err.message}`);
      });
  };

  useEffect(() => {
    fetchData();
    const intervalId = setInterval(fetchData, 60000);
    return () => clearInterval(intervalId);
  }, [refresh]);

  const handleRefreshClick = () => {
    setRefresh((prev) => !prev);
  };

  return (
    <div className="App-container">
      <Navbar onRefreshClick={handleRefreshClick} />
      <div className="App">
        <h1>現在時刻</h1>
        <CurrentTime />
        <h1>予測データ</h1>
        {error ? (
          <p style={{ color: "red" }}>{error}</p>
        ) : data ? (
          <div className="box-container">
            <Box value={data.prediction.toFixed(1)} unit="分" label="ただいまの予測待ち時間" />
            <Box value={data.weather} label="天気" />
            <Footer timestamp={data.timestamp} />
          </div>
        ) : (
          <p>データを読み込み中...</p>
        )}
      </div>
    </div>
  );
}

export default App;
