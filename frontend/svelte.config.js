import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    kit: {
        adapter: adapter({
            fallback: 'index.html',
            precompress: false,
            strict: false
        }),
        paths: {
            base: ''
        }
    },
    preprocess: vitePreprocess()
};

export default config;
