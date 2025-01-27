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

When cells of differing colours are placed, the new generation will have cells of the colour that is an average of the neighbouring cells.

## How to run project


## How to buid project


## How to test project


## Decisions
- Websockets as the transport layer for real-time updates and support multiple clients
- Github Actions for CI/CD
- Terraform for IaC with AWS as infrastructre provider
    - ECS for deploying dockerised backend
    - Load balancer in front of ECS
    - S3 + Cloudfront for frontend
- Dockerised backend and deployed on ECS for managed servivce
    - Python
- Frontend to be deployed as built files onto S3 + Cloudfront
    - Svelte + Typescript
- Used mathemematical average of neighbouring cells to determine colour of new cells
- Game board will be limited to 100x100 to explore some interesting patterns
- Game board will not be toroidal to simplify calcuations for this iteration
- Using a sparse calculation approach as not all cells will be live, don't iterate over dead cells
