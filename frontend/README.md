# Game of Life Frontend

This is the frontend application for Conway's Game of Life, built with SvelteKit and TypeScript.

## Development Setup

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm run dev
```

## Code Quality Tools

### ESLint

We use ESLint for static code analysis with TypeScript and Svelte support.

Available commands:

- Check for issues:

```bash
npm run lint
```

- Fix automatically fixable issues:

```bash
npm run lint:fix
```

### Prettier

Prettier is configured for consistent code formatting across the project.

Available commands:

- Format all files:

```bash
npm run format
```

- Check formatting without making changes:

```bash
npm run format:check
```

Configuration files:

- `.prettierrc` - Prettier configuration
- `.prettierignore` - Files to be ignored by Prettier

### Pre-commit Hooks

We use Husky and lint-staged to ensure code quality before commits. The setup process is automated for cross-platform compatibility.

#### Setup Instructions

1. Install dependencies (this will also set up husky):

```bash
npm install
```

2. If the pre-commit hooks are not installed automatically, run:

```bash
npm run prepare
```

#### Troubleshooting

If you encounter permission issues on Unix-like systems (Linux/macOS):

1. Make the husky scripts executable:

```bash
chmod ug+x .husky/*
```

2. Ensure Git hooks are enabled:

```bash
git config core.hooksPath .husky
```

For Windows users:

- Ensure you have Git Bash installed
- Run the terminal as administrator if you encounter permission issues
- Use PowerShell or Git Bash instead of CMD

The pre-commit hooks will:

- Format all staged files with Prettier
- Run ESLint on all staged JavaScript, TypeScript, and Svelte files
- Block commits if there are any linting errors

Configuration files:

- `package.json` - Contains the lint-staged configuration
- `.husky/pre-commit` - The pre-commit hook script (this should be committed to version control)

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run check` - Run Svelte type checking
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Run ESLint with auto-fix
- `npm run format` - Format code with Prettier
- `npm run format:check` - Check code formatting

## Project Structure

```
src/
├── lib/           # Shared components and utilities
├── routes/        # SvelteKit routes and page components
└── app.html       # Main HTML template
```

## Code Style Guidelines

- Use TypeScript for type safety
- Follow Svelte's component structure guidelines
- Keep components focused and modular
- Use CSS modules for component-specific styles
- Follow accessibility best practices

## Contributing

1. Ensure you have Node.js and npm installed
2. Fork and clone the repository
3. Install dependencies: `npm install`
4. Create a feature branch
5. Make your changes
6. Run tests and ensure linting passes
7. Commit your changes (this will trigger pre-commit hooks)
8. Push to your fork and submit a pull request
