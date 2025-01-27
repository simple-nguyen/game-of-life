# Conway's Game of life

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

## How to run project
Note: Copy the .env.example into .env and set accordingly the env variables

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

The game will be available at http://localhost:5173

## How to build project

### Backend
```bash
cd backend
docker build -t game-of-life-backend .
docker run -p 8000:8000 game-of-life-backend
```

### Frontend
```bash
cd frontend
npm run build
```

## How to test project

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

## Decisions
- Websockets as the transport layer for real-time updates and support multiple clients
- Github Actions for CI/CD
- Terraform for IaC with AWS as infrastructre provider
    - ECS for deploying dockerised backend
    - Load balancer in front of ECS
    - S3 + Cloudfront for frontend
- Dockerised backend and deployed on ECS for managed service
    - Python
- Frontend to be deployed as built files onto S3 + Cloudfront
    - Svelte + Typescript
    - Grid will be drawn on HTML Canvas
- Used mathemematical average of neighbouring cells to determine colour of new cells
- Game board will be limited to 100x100 to explore some interesting patterns
- Game board will not be toroidal to simplify calcuations for this iteration
- Using a sparse calculation approach as not all cells will be live, don't iterate over dead cells

## Challenges / Interesting Encounters
- Decent AI initialise of project