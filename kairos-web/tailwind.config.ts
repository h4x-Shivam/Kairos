import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        bg: {
          primary: "#07090E",
          secondary: "#0D111A",
          tertiary: "#141A26",
        },
        grey: {
          100: "#F5F5F5",
          300: "#B3B3B3",
          500: "#737373",
          700: "#404040",
          900: "#1A1A1A",
        },
        text: {
          primary: "#FFFFFF",
          secondary: "#A3A3A3",
          tertiary: "#6B6B6B",
        },
        border: {
          subtle: "rgba(255, 255, 255, 0.10)",
          active: "rgba(255, 255, 255, 0.24)",
        },
        signal: {
          good: "#EAB308",      // Yellow — reserved exclusively for HOLD verdict
          critical: "#DC2626",  // Red — reserved exclusively for Tier-1 Critical/Emergency
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
        display: ["var(--font-display)", "Impact", "sans-serif"],
        mono: ["var(--font-mono)", "JetBrains Mono", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;
