import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [
        ElementPlusResolver(),
      ],
    }),
    Components({
      resolvers: [
        ElementPlusResolver(),
      ],
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  build: {
    chunkSizeWarningLimit: 500,
    cssCodeSplit: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vue: ["vue", "vue-router"],
        },
        chunkFileNames: (chunkInfo) => {
          if (chunkInfo.moduleIds[0].includes("node_modules")) {
            return "assets/vendor-[hash].js";
          }
          return "assets/index-[hash].js";
        },
      },
    },
    brotliSize: false,
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
