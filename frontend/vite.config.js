import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  build:{
    sourcemap:false
  },
  server: {
    proxy: {
      // All requests starting with /api go to backend
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        // optional: rewrite removes /api prefix if your backend doesn't expect it
        // rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
