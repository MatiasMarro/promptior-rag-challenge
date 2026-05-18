/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          'bg-base': '#0B0F19',
          'bg-surface': '#151B2C',
          'bg-elevated': '#1F2937',
          border: '#1F2937',
          'text-primary': '#F9FAFB',
          'text-secondary': '#9CA3AF',
          accent: '#00E5FF',
          'accent-hover': '#22D3EE',
          'accent-muted': '#0891B2',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
