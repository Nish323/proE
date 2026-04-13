import { useEffect, useState } from "react";
import "./CurrentTime.css";

export function CurrentTime() {
  const [currentTime, setCurrentTime] = useState<string>("");

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      const hours = String(now.getHours()).padStart(2, "0");
      const minutes = String(now.getMinutes()).padStart(2, "0");
      setCurrentTime(`${hours}:${minutes}`);
    };

    updateTime();
    const intervalId = setInterval(updateTime, 1000); // 1秒ごとに時刻を更新

    return () => clearInterval(intervalId); // クリーンアップ
  }, []);

  return <div className="current-time">{currentTime}</div>;
}
