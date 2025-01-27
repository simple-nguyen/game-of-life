import eslint from '@eslint/js';
import tseslint from '@typescript-eslint/eslint-plugin';
import tsparser from '@typescript-eslint/parser';
import sveltePlugin from 'eslint-plugin-svelte';
import * as svelteParser from 'svelte-eslint-parser';
import prettierConfig from 'eslint-config-prettier';

export default [
    eslint.configs.recommended,
    {
        files: ['**/*.{ts,js}'],
        plugins: {
            '@typescript-eslint': tseslint
        },
        languageOptions: {
            parser: tsparser,
            parserOptions: {
                ecmaVersion: 2020,
                sourceType: 'module'
            },
            globals: {
                window: true,
                document: true,
                WebSocket: true
            }
        },
        rules: {
            '@typescript-eslint/no-explicit-any': 'warn',
            '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
            'no-console': ['warn', { allow: ['warn', 'error'] }],
            'no-case-declarations': 'off'
        }
    },
    {
        files: ['**/*.svelte'],
        plugins: {
            svelte: sveltePlugin
        },
        languageOptions: {
            parser: svelteParser,
            parserOptions: {
                parser: tsparser
            }
        },
        rules: {
            ...sveltePlugin.configs.recommended.rules,
            'svelte/no-at-html-tags': 'error',
            'no-undef': 'off'
        }
    },
    prettierConfig
];
