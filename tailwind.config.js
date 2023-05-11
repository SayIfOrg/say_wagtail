/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./say/**/templates/**/*.{html,js,ts,jsx,tsx}",

    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
}
