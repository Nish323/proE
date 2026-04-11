import "./Navbar.css";
import { RefreshCcw } from "lucide-react";

// propsの型を定義
type NavbarProps = {
  onRefreshClick: () => void;
};

export function Navbar({ onRefreshClick }: NavbarProps) {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <img 
          src="/logo.png" 
          alt="PALTO-AI Logo" 
          className="logo"
        />
      </div>
      <button onClick={onRefreshClick} className="navbar-button">
        <RefreshCcw className="navbar-button-icon" />
        <p className="navbar-button-text">Update</p>
      </button>
    </nav>
  );
}
