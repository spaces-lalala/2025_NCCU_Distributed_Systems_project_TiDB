import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5002,
    host: '127.0.0.1',
  },
  resolve: {
    alias: [
      { find: '@', replacement: '/src' }
    ]
  },
});