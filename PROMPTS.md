This is a list of prompts used within this project, by order of usage. I will commmit the code after every prompt and note if AI used or not:

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