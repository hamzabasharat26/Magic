/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './accounts/templates/**/*.html',
    './measurements/templates/**/*.html',
    './products/templates/**/*.html',
    './**/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        // Industrial Professional Palette
        'industrial': {
          'blue-dark': '#2c3e50',
          'blue-light': '#3498db',
          'blue-primary': '#667eea',
          'purple': '#764ba2',
          'green': '#10B981',
          'green-light': '#34D399',
          'red': '#EF4444',
          'red-dark': '#DC2626',
          'yellow': '#F59E0B',
          'gray-50': '#FAFBFC',
          'gray-100': '#F8FAFC',
          'gray-200': '#E2E8F0',
          'gray-300': '#CBD5E1',
          'gray-400': '#94A3B8',
          'gray-500': '#64748B',
          'gray-600': '#475569',
          'gray-700': '#334155',
          'gray-800': '#1E293B',
        },
      },
      fontFamily: {
        'inter': ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
      },
      boxShadow: {
        'industrial': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'industrial-lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'industrial-colored': '0 10px 15px -3px rgba(102, 126, 234, 0.3)',
      },
      minHeight: {
        'touch': '48px', // Operator panel touch targets
      },
    },
  },
  plugins: [],
}
