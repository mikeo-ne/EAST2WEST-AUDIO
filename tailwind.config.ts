import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        studio: "#0D0F12",
        gold: "#F59E0B",
        teal: "#2DD4BF"
      },
      boxShadow: {
        glow: "0 0 28px rgba(245, 158, 11, 0.18)"
      }
    }
  },
  plugins: []
};

export default config;
