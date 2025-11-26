/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        accent: '#00bcd4',
        bg: '#0e0e11',
        card: '#18181c',
        text: '#e0e0e0',
        subtext: '#9aa0a6',
        hover: '#1f1f23',
      },
      fontFamily: {
        poppins: ['Poppins', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
