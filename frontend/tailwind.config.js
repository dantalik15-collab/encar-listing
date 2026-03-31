/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          dark: "#0a0a0a",
          card: "#141414",
          border: "#262626",
          accent: "#c8a96e",
          "accent-light": "#dbc291",
          muted: "#737373",
          light: "#e5e5e5",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
