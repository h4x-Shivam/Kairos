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
          primary: "#FFFFFF",
          secondary: "#FAFAFA",
          tertiary: "#F3F4F6",
        },
        grey: {
          100: "#111111", // inverted for light theme
          300: "#374151",
          500: "#6B7280",
          700: "#E5E7EB",
          900: "#F3F4F6", // light grey for backgrounds
        },
        text: {
          primary: "#111111",
          secondary: "#4B5563",
          tertiary: "#9CA3AF",
        },
        border: {
          subtle: "#E5E7EB",
          active: "#D1D5DB",
        },
        signal: {
          hold: "#166534",      // Deep Green
          tighten: "#1D4ED8",   // Blue
          trim25: "#D97706",    // Amber
          trim50: "#C2410C",    // Orange
          exit: "#DC2626",      // Red
          good: "#166534",      // legacy fallback
          critical: "#DC2626",  // legacy fallback
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
