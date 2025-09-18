import vue from "@vitejs/plugin-vue";

import path from "path";
import { defineConfig } from "vite";
import vuetify from "vite-plugin-vuetify";

export default defineConfig({
  plugins: [vue(), vuetify({ autoImport: true })],
  base: "/view/",
  server: {
    allowedHosts: true,
    host: "0.0.0.0",
    strictPort: false,
    watch: {
      usePolling: true,
      interval: 1000,
    },
  },
  build: {
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, "index.html"),
      },
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
});
