import "./Box.css";

type BoxProps = {
	value: string | number;
	unit?: string;
	label: string;
};

export function Box(props: BoxProps) {
	return (
		<div className="status-card">
        <div className="status-top">
				{typeof props.value === "number" ? (
					<span className="percentage">{props.value}<span className="unit">{props.unit || "%"}</span></span>
				) : (
					<span className="percentage">{props.value}</span>
				)}
        </div>
        <div className="status-bottom">
            <span className="label">{props.label}</span>
        </div>
    </div>
	);
}