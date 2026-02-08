/** @type {import('tailwindcss').Config} */
export default {
  // Especifica quais arquivos o Tailwind deve varrer para encontrar classes
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    // Estende o tema padrão do Tailwind com cores e configurações customizadas
    extend: {
      colors: {
        // Cores customizadas para a aplicação
        primary: '#3b82f6',
        secondary: '#10b981',
        danger: '#ef4444',
      }
    },
  },
  plugins: [],
}
