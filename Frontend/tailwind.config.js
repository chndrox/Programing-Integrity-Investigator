export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Light theme
        'light-bg': '#F8FAFC',
        'light-sidebar': '#FFFFFF',
        'light-card': '#FFFFFF',
        'light-primary': '#4F46E5',
        'light-text': '#0F172A',
        'light-border': '#E2E8F0',
        // Dark theme
        'dark-bg': '#0B1120',
        'dark-sidebar': '#111827',
        'dark-card': '#172033',
        'dark-primary': '#818CF8',
        'dark-text': '#F8FAFC',
        'dark-border': '#293548',
      },
    },
  },
  plugins: [],
}
