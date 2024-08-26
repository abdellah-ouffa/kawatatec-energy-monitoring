/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./energy_monitoring/core/templates/**/*.html",
    "./energy_monitoring/core/static/**/*.js",
    "./energy_monitoring/**/*.html",
    // Add this line to include the template directory
    "./template/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        'kawata-blue': '#3b82f6', // Adjust this hex code to match the exact blue in the Kawatatec logo
      }
    },
  },
  plugins: [],
}

