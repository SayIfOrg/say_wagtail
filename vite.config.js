import {defineConfig} from "vite";
import { resolve } from "path"


export default defineConfig({
  root: resolve('say'),
  base: '/static/',
  server: {
    host: 'localhost',
    port: 8001,
  },
  build: {
    outDir: resolve('say/static_dist'),
    manifest: true,
    emptyOutDir: true,
    rollupOptions: {
      // overwrite default .html entry
      input: {
        main: resolve('say/static_src/main.ts'),
      },
    },
  }
})