import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// El backend FastAPI corre en :8000 durante el desarrollo.
// Proxyeamos las rutas del API para poder usar paths relativos tanto en
// dev como en prod (donde el mismo FastAPI sirve el frontend buildeado).
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/promtior': 'http://localhost:8000',
      '/health': 'http://localhost:8000',
    },
  },
})
