import "./Footer.css";

type FooterProps = {
  timestamp: string;
};

export function Footer({ timestamp }: FooterProps) {
  return (
    <footer className="footer">
      <p>Last Updated: {timestamp}</p>
    </footer>
  );
}
