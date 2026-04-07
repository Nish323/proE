import React from "react";
import "./Navbar.css";
import axios, { AxiosError } from "axios";
import { useState, useEffect } from "react";
import { RefreshCcw } from "lucide-react";

type PredictionData = {
  prediction: string;
  timestamp: string;
};

export function Navbar() {
  const [data, setData] = useState<PredictionData | null>(null);
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
    <nav className="navbar">
      <div className="navbar-logo">
        <div className="navbar-main-logo">PALTO-AI</div>
        <div className="navbar-sub-logo">crowd view</div>
      </div>
      <button onClick={handleRefreshClick} className="navbar-button">
        <RefreshCcw className="navbar-button-icon" />
        <p className="navbar-button-text">Update</p>
      </button>
    </nav>
  );
}
