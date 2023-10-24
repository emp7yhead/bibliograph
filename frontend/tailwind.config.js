import { nextui } from '@nextui-org/react';

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
    './node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    container: {
      center: true,
    },
    extend: {
      colors: {
        default: '#e7ecef',
        background: '#e7ecef',
        primary: '#274c77',
        secondary: '#6096ba',
        success: '#a3cef1',
        warning: '#8b8c89',
        error: 'oklch(54% 0.22 29)',
      },
    },
  },
  darkMode: 'class',
  plugins: [nextui()],
};
