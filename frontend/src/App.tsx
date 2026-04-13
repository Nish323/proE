import React from "react";
// import logo from "./logo.svg";
import "./App.css";
import axios, { AxiosError } from "axios"; // AxiosErrorをインポート
import { useEffect, useState } from "react";
import { Navbar } from "./components/Navbar/Navbar";
import { Box } from "./components/Box/Box";
import { Footer } from "./components/Footer/Footer";
import { CurrentTime } from "./components/CurrentTime/CurrentTime";

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

  // errorをないことにする
  error && setError(null);

  // 仮データ
  const mockData: PredictionData = {
    prediction: "混雑度は高めです",
    timestamp: "11:58",
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
        ) : mockData.prediction ? ( // data自体ではなく、data.predictionの存在をチェック
          <div className="box-container">
            <Box value={10} unit="分" label="ただいまの予測待ち時間" />
            <Box value="晴れ" label="ただいまの天気" />
          </div>
        ) : (
          <p>データを読み込み中...</p>
        )}
      </div>
      <Footer timestamp={mockData.timestamp} />
    </div>
  );
}

export default App;
