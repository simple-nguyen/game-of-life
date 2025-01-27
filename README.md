# Conway's Game of Life

## Problem
This project implements Conway's Game of Life with a multiplayer aspect. The principles of the Game of Life are as follows:

1. Any live cell with fewer than two live neighbors dies, as
if caused by under-population.
2. Any live cell with two or three live neighbors lives on to
the next generation.
3. Any live cell with more than three live neighbors dies, as
if by overcrowding.
4. Any dead cell with exactly three live neighbors becomes
a live cell, as if by reproduction.

Multiple players can join an instance of the game and place live cells in the browser. The game will be played out in real-time, with the next generation being calculated every 1 second.

When a player joins, they will be assigned a random colour. A player will be identified by their username. A player's cells will live on irrespective of their connection status.

When cells are reproduced, the new generation will have cells of the colour that is an average of the neighbouring cells.

## Quick Start with Docker Compose

The easiest way to run the entire application:

```bash
# Copy environment file
cp .env.example .env

# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

The application will be available at:
- Frontend: http://localhost:80
- Backend API: http://localhost:8000
- WebSocket: ws://localhost:8000/ws

## Development Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

The backend includes:
- FastAPI for the REST API and WebSocket server
- Automatic code formatting with black and isort
- Linting with flake8
- Testing with pytest

### Frontend
```bash
cd frontend
npm install
npm run dev
```

The frontend includes:
- SvelteKit for the UI
- TypeScript for type safety
- ESLint and Prettier for code quality
- Husky for pre-commit hooks

The development server will be available at http://localhost:5173

### Git Hooks

This project uses Husky for managing Git hooks. The hooks are automatically installed when you run `npm install` in the root directory. These hooks ensure code quality by:

- Running ESLint and Prettier on staged frontend files
- Running Black, isort, and flake8 on staged Python files

The hooks will run automatically before each commit. Make sure to install the dependencies in the root directory:

```bash
npm install  # Install husky and other dev dependencies
```

## Code Quality

### Backend
- Automatic formatting with black and isort
- Linting with flake8 (including docstring checks)
- Pre-commit hooks for Python files

Run checks manually:
```bash
cd backend
black .
isort .
flake8 .
```

### Frontend
- ESLint for JavaScript/TypeScript linting
- Prettier for code formatting
- Pre-commit hooks for all frontend files

Run checks manually:
```bash
cd frontend
npm run lint
npm run format
```

## Testing

### Backend
```bash
cd backend
pytest --cov=src tests/
```

### Frontend
```bash
cd frontend
npm run test
```

## Building for Production

### Using Docker Compose (Recommended)
```bash
# Build all services
docker-compose build

# Run in production mode
docker-compose up -d
```

### Individual Services

Backend:
```bash
cd backend
docker build -t game-of-life-backend .
docker run -p 8000:8000 game-of-life-backend
```

Frontend:
```bash
cd frontend
docker build -t game-of-life-frontend .
docker run -p 80:80 game-of-life-frontend
```

## Architecture Decisions
- WebSockets for real-time updates and multiple clients
- GitHub Actions for CI/CD
- Terraform for IaC with AWS as infrastructure provider
    - ECS for deploying dockerized backend
    - Load balancer in front of ECS
    - S3 + CloudFront for frontend
- Dockerized services with Docker Compose for easy deployment
    - Python backend with FastAPI
    - SvelteKit frontend with Nginx
- Used mathematical average of neighbouring cells for new cell colors
- Game board limited to 100x100 for interesting patterns
- Non-toroidal board for simplified calculations
- Sparse calculation approach for performance optimization

## Project Structure
```
.
├── backend/                 # Python FastAPI backend
│   ├── src/                # Source code
│   ├── tests/              # Test files
│   ├── Dockerfile         # Backend container definition
│   └── requirements.txt   # Python dependencies
├── frontend/               # SvelteKit frontend
│   ├── src/               # Source code
│   ├── static/            # Static assets
│   └── Dockerfile        # Frontend container definition
├── docker-compose.yml     # Multi-container definition
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure all checks pass
5. Submit a pull request

## Challenges / Interesting Encounters
- Decent AI initialization of project
- Managing real-time state across multiple clients
- Color inheritance calculations
- Docker configuration for development and production
- Cross-service communication setup