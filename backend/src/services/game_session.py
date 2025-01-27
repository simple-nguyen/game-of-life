from typing import Dict, List
from fastapi import WebSocket
import asyncio
import logging
from .game_loop import GameLoop

logger = logging.getLogger(__name__)

COLORS = [
    "#FF0000", "#00FF00", "#0000FF", "#FF00FF", 
    "#00FFFF", "#FFA500", "#800080", "#008000",
    "#FFC0CB", "#FFD700", "#4B0082", "#7B68EE"
]

class GameSession:
    def __init__(self):
        """Initialize a new game session."""
        self.users: Dict[str, WebSocket] = {}
        self.user_colors: Dict[str, str] = {}
        self.game_loop = GameLoop()
        self.game_task = None
        self.running = False
        logger.info("New game session created")

    def set_and_get_user_color(self, username: str):
        if username in self.user_colors:
            return self.user_colors[username]
        else:
            color = COLORS[len(self.user_colors) % len(COLORS)]
            self.user_colors[username] = color
            return color

    async def add_user(self, username: str, websocket: WebSocket) -> List[Dict[str, str]]:
        """Add a user to the session.
        
        Args:
            username: User's identifier
            websocket: User's WebSocket connection
        """
        self.set_and_get_user_color(username)
        self.users[username] = websocket
        logger.info(f"User {username} joined the session")
        
        if not self.running:
            await self.start_game()
        
        # Send current game state to the new user
        await self.send_game_state(username)

        # Return list of user color dictionaries
        return [{"username": user, "color": color} for user, color in self.user_colors.items()]

    async def remove_user(self, username: str) -> None:
        """Remove a user from the session.
        
        Args:
            username: User's identifier
        """
        if username in self.users:
            logger.info(f"User {username} left the session")
            del self.users[username]

    def has_users(self) -> bool:
        """Check if the session has any users.
        
        Returns:
            bool: True if there are users, False otherwise
        """
        return len(self.users) > 0

    async def handle_message(self, username: str, data: dict) -> None:
        """Handle a message from a user.
        
        Args:
            username: User's identifier
            data: Message data
        """
        message_type = data.get('type')
        
        if message_type == 'place_cell':
            x = data.get('x')
            y = data.get('y')
            if x is not None and y is not None:
                self.game_loop.place_cell(x, y, username)
                await self.broadcast_game_state()

    async def broadcast(self, message: dict) -> None:
        disconnected_users = []
        for username, websocket in self.users.items():
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to {username}: {str(e)}")
                disconnected_users.append(username)
        
        for username in disconnected_users:
            logger.info(f"Removing disconnected user: {username}")
            self.remove_user(username)

    async def broadcast_game_state(self) -> None:
        """Broadcast the current game state to all users."""
        if not self.users:
            return

        state = self.game_loop.get_state()
        message = {
            'type': 'game_state',
            'state': state
        }

        for websocket in self.users.values():
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting game state: {str(e)}")

    async def send_game_state(self, username: str) -> None:
        """Send the current game state to a specific user.
        
        Args:
            username: User's identifier
        """
        if username not in self.users:
            return

        state = self.game_loop.get_state()
        message = {
            'type': 'game_state',
            'state': state
        }

        try:
            await self.users[username].send_json(message)
        except Exception as e:
            logger.error(f"Error sending game state to {username}: {str(e)}")

    def start_game_loop(self) -> None:
        """Start the game loop."""
        if not self.running:
            self.running = True
            self.game_task = asyncio.create_task(self._run_game_loop())
            logger.info("Game loop started")

    def stop_game_loop(self) -> None:
        """Stop the game loop."""
        if self.running:
            self.running = False
            if self.game_task:
                self.game_task.cancel()
            logger.info("Game loop stopped")

    async def _run_game_loop(self) -> None:
        """Run the game loop."""
        while self.running:
            try:
                self.game_loop.next_generation()
                await self.broadcast_game_state()
                await asyncio.sleep(1)  # Update every second
            except Exception as e:
                logger.error(f"Error in game loop: {str(e)}")
                await asyncio.sleep(1)  # Wait before retrying

    async def start_game(self) -> None:
        """Start the game."""
        self.start_game_loop()
