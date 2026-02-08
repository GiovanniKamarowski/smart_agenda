import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Configuração do servidor de desenvolvimento
    port: 5173,
    // Proxy para a API do FastAPI (evita erros de CORS no desenvolvimento)
    proxy: {
      // Qualquer requisição que começar com /api será enviada para http://localhost:8000
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
