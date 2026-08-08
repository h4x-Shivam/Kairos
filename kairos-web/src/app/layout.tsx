import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Kairos — Algorithmic When to Sell Engine",
  description:
    "Deterministic quantitative exit discipline and downside protection engine for Indian equities.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-bg-primary text-text-primary min-h-screen antialiased">
        {children}
      </body>
    </html>
  );
}
