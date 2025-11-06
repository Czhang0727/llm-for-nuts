import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

function resolve(dir: string) {
  return path.join(__dirname, '.', dir)
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // 配置别名
  resolve: {
    alias: {
      '@': resolve('src'), // 设置 `@` 指向 `src` 目录
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
})
