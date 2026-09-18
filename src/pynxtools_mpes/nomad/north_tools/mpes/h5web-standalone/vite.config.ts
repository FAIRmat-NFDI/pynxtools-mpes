import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

// Built once at image-build time and served locally (see config/h5web-view) -
// a relative base keeps the built asset paths working regardless of which
// local port ends up serving them.
export default defineConfig({
  base: './',
  plugins: [react()],
});
