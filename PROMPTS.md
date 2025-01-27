This is a list of prompts used within this project, by order of usage. I will commmit the code after every prompt and note if AI used or not: (model: claude3.5)

```
Based on the project readme, initalise my project, including .github, terraform, backend and frontend
```

Now to initalise backend code to give us a good start to filling out the requirements to serve a websocket server for our Game of Life

```Initialise by backend such that I have the following:
- main.py which initialises websocket server
- services/websocket_service.py which controls that data transfer we need and generates game_sessions for each connection of a new session
- services/game_session to manage the game session and manage the game loop
- services/game_loop to manage the conway game of life logic 
```

Now we do the same for the frontend
```
now we will focus on the frontend. we want to ensure the app has structured directories for components, services and utilities

- login page that will start the game session via connected websocket, a user can set their username and channel code to start if iti isi available, if not the create a channel (update backend to include this message)
- game page where it will show a nav with the Game of Life title, username and channel code
- left side nav where we can show connected users, the currently set colour of the player (assiigned by backend)
- canvas where a user can select and colour cells

the frontend is a svelte project
```

Find and fix initialisation of frontend boostrapping
```
check the entirety of frontend and ensure all necessary files are created to initialise the app
```

Adding linting and documentation
```
add linter for python
add a readme in backend
```

Adding linting on frontend and update readme
```
add linter frontend for svelte and typescript, use esconfig.config.js
```

Updating readme for frontend
```
Update readme for frontend for linting / pre-commit
Update package.json to install husky per OS which can be different
```

Adding precommit for python
```
Added pre-commit to python, keep files in the backend
Fix error 
[ERROR] Cowardly refusing to install hooks with `core.hooksPath` set.
```

Adding dockerfile to frontend for ease of installation / running
Update our backend at same time
Add docker-compose.yml
Update root readme
```
Add dockerfile to frontend
Update backend dockerfile to match existing codebase
Added docker-compose.yml to run from root for both backend and frontend
Fix husky in dockerfile
Fix husky in local development for any os
Update root README
```