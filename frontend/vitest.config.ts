import { defineConfig } from 'vitest/config'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import path from 'path'

export default defineConfig({
    plugins: [svelte({ hot: !process.env.VITEST })],
    test: {
        include: ['tests/**/*.{test,spec}.{js,ts}'],
        environment: 'jsdom',
        setupFiles: ['tests/setup.ts'],
        deps: {
            inline: ['@testing-library/svelte'],
        },
    },
    resolve: {
        alias: {
            $lib: path.resolve(__dirname, './src/lib'),
        },
    },
})
