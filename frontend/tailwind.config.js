/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          cyan: "#00F0FF",
          blue: "#00A6FA",
          gold: "#FFD700",
          dark: "#0A0A0B",
          card: "#111113",
        },
      },
      backgroundImage: {
        'gradient-brand': 'linear-gradient(to right, #00F0FF, #00A6FA)',
        'gradient-gold': 'linear-gradient(to right, #FFD700, #F59E0B)',
      },
    },
  },
  plugins: [],
}
