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
        <div className="navbar-main-logo">PALTO-AI</div>
        <div className="navbar-sub-logo">crowd view</div>
      </div>
      <button onClick={onRefreshClick} className="navbar-button">
        <RefreshCcw className="navbar-button-icon" />
        <p className="navbar-button-text">Update</p>
      </button>
    </nav>
  );
}
