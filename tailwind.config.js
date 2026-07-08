/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        obsidian: "#07080c",
        panel: "#10131b",
        panelSoft: "#171b25",
        stroke: "#2a3040",
        ember: "#f97316",
        gold: "#d7b56d",
        cyan: "#6ee7f9"
      },
      boxShadow: {
        studio: "0 24px 80px rgba(0,0,0,0.45)"
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"]
      }
    }
  },
  plugins: []
};