import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		host: true,
		port: 5173,
		strictPort: true
	},
	preview: {
		port: 5173,
		strictPort: true
	},
	build: {
		target: 'esnext',
		outDir: '.svelte-kit/output',
		assetsDir: 'assets',
		sourcemap: true
	}
});
