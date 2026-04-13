import { useState } from "react";
import "./Navbar.css";
import { RefreshCcw } from "lucide-react";

// propsの型を定義
type NavbarProps = {
  onRefreshClick: () => void;
};

export function Navbar({ onRefreshClick }: NavbarProps) {
  const [isRotating, setIsRotating] = useState(false);

  const handleButtonClick = () => {
    setIsRotating(true);
    onRefreshClick();
    setTimeout(() => {
      setIsRotating(false);
    }, 600);
  };

  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <img src="/logo.png" alt="PALTO-AI Logo" className="logo" />
      </div>
      <button onClick={handleButtonClick} className="navbar-button">
        <RefreshCcw
          className={`navbar-button-icon ${isRotating ? "rotating" : ""}`}
        />
        <p className="navbar-button-text">Update</p>
      </button>
    </nav>
  );
}
