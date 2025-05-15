        // vite.config.ts
        import { defineConfig } from 'vite'
        import vue from '@vitejs/plugin-vue'
        import path from 'path' // 確保引入 path

        export default defineConfig({
          plugins: [vue()],
          resolve: {
            alias: {
              '@': path.resolve(__dirname, './src'),
            },
          },
          server: {
            port: 5002, // Changed port to 5174
            proxy: {
              '/api': {
                target: 'http://localhost:8000', // 指向您的模擬後端
                changeOrigin: true,
                // rewrite: (path) => path.replace(/^\/api/, '') // 移除 /api 前綴
              },
            }
          }
        })