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

Requirements:
- Docker and Docker Compose

The application will be available at:
- Frontend: http://localhost:80
- Backend API: http://localhost:8000
- WebSocket: ws://localhost:8000/ws

## Development Setup

### Backend
Requirements:
- Python 3.10 or higher
- pip

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOL
CORS_ORIGINS=http://localhost:5173
EOL

# Start development server
uvicorn src.main:app --reload
```

The backend includes:
- FastAPI for the REST API and WebSocket server
- Automatic code formatting with black and isort
- Linting with flake8 (including docstring checks with flake8-docstrings)
- Testing with pytest and pytest-cov

### Frontend
Requirements:
- Node.js 18 or higher
- npm

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cat > .env << EOL
BACKEND_URL=http://localhost:8000
EOL

# Start development server
npm run dev
```

The frontend includes:
- SvelteKit for the UI
- TypeScript for type safety
- ESLint and Prettier for code quality
- Vitest and Testing Library for testing
- Static adapter for production builds

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
# Create production .env file
cat > .env << EOL
CORS_ORIGINS=http://localhost:80,http://frontend:80
BACKEND_URL=http://backend:8000
EOL

# Build all services
docker-compose build

# Run in production mode
docker-compose up -d
```

### Individual Services

Backend:
```bash
cd backend

# Create production .env file
cat > .env << EOL
CORS_ORIGINS=http://localhost:80
EOL

# Build Docker image
docker build -t game-of-life-backend .

# Run container
docker run -p 8000:8000 \
  --env-file .env \
  game-of-life-backend
```

Frontend:
```bash
cd frontend

# Create production .env file
cat > .env << EOL
BACKEND_URL=http://localhost:8000
EOL

# Build Docker image
docker build -t game-of-life-frontend .

# Run container
docker run -p 80:80 \
  --env-file .env \
  game-of-life-frontend
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
- Game board limited to 50x30 for interesting patterns
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

## Challenges / Interesting Encounters / Thoughts
- Went full in on the deep end as I haven't worked with Python and Svelte in detail before. Took a bit of time getting my head around syntax and patterns. AI helped me get up to speed as it gave me example code.
- Decent AI initialization of project but left a lot of work to complete
    - Decent time savings
- Docker configuration for development and production took some time to figure out the correct setup
- Cross-service communication setup
- Implementing the Conway algorithm was fun, I did some reading up prior to starting and went with the sparse approach. I believe this was a fairly-optimal solution for the project as most of the time it was would sparse or converge to sparse grid.
- AI did a good job of initialising backend test, frontend needed much more manual intervention
- While I didn't get to complete the deployment to AWS, I believe running in ECS is a good first attempt, this will involve ensuring a domain would be setup to smooth out the process of assigning Route53 records to the service and thus point frontend/backend uris correctly.
- Went with only passing up updates per cell changes instead of the entire grid to ensure scalability if the grid grew large where the cells are sparse. This reduces the number of updates we need to draw for the number of cells that are alive.
- Opted for hardcoded grid size which would mostly fit my laptop screen size, this can definitely be customised depending on resolution though opted for this for initial attempt
- Colors could also be generated randomly but I figured a set of hardcoded colours per player was acceptable which would loop around if it ran out. If the game grew much larger, could look at optimising and allowing choice
- The currently session are "stored" in memory based on username for speed of lookoup. However, with game configurations likely to persist if there were other settings such as custom colour, then we would want to store it in a DB
- Should have written tests earlier instead of leaving it until the end. It did pick up on one error I could have missed with the incorrect color coming through which would not have been rendered correctly.

## To Do
After sef-imposed 8 hour limit here are some of the things that I needed left to complete for full production ready build

- Fully flesh out more tests to have more coverage, opted for most logic heavy parts of code
- Finalize Terraform and deploy to AWS account
    - Will involve ensuring we have correct domains being passed through as env variables for backend uri
- Setup Github Actions to apply terraform changes and deploy code (backend and frontend)
    - Using Github Secrets to store most of our deployment secrets to connect to AWS for Terraform deployment