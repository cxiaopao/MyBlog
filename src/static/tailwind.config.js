/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../templates/*.html", "../templates/**/*.html"],
  theme: {
    container:{
      center: true,
      screens: {
        md: "1120px",
        lg: "1120px",
        xl: "1120px",
        "2xl": "1120px",
      }
    },
    extend: {
      colors:{
        'primary': '#FF6363',
        'secondary': "#FFA63D",
        "tertiary": "#FFD700",
        "blog-dark": "#2B2A4C",
      }
    },
  },
  plugins: [],
}

