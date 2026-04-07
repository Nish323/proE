import React from "react";
import "./Navbar.css";
import { RefreshCcw } from "lucide-react";

export function Navbar() {
	return (
		<nav className="navbar">
			<div className="navbar-logo">
				<div className="navbar-main-logo">PALTO-AI</div>
				<div className="navbar-sub-logo">crowedview</div>
			</div>
			<button className="navbar-button">
				<RefreshCcw />
				<p>Update</p>
			</button>
		</nav>
	);
}