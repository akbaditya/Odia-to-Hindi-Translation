/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#f4f7fb",
          100: "#e6ecf5",
          200: "#c9d6e8",
          300: "#a3b8d6",
          400: "#7893bd",
          500: "#5573a3",
          600: "#425c87",
          700: "#374b6e",
          800: "#2e3e5a",
          900: "#1f2a3d",
        },
        surface: {
          light: "#ffffff",
          soft: "#f6f8fb",
          border: "#e3e8f0",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        odia: ["Noto Sans Oriya", "sans-serif"],
        hindi: ["Noto Sans Devanagari", "sans-serif"],
      },
      borderRadius: {
        xl2: "1.1rem",
      },
    },
  },
  plugins: [],
};