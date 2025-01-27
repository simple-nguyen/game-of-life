from typing import Dict, List
from fastapi import WebSocket
import asyncio
import logging
from .game_loop import GameLoop

logger = logging.getLogger(__name__)

class GameSession:
    def __init__(self):
        """Initialize a new game session."""
        self.users: Dict[str, WebSocket] = {}
        self.game_loop = GameLoop()
        self.game_task = None
        self.running = False
        logger.info("New game session created")

    async def add_user(self, username: str, websocket: WebSocket) -> None:
        """Add a user to the session.
        
        Args:
            username: User's identifier
            websocket: User's WebSocket connection
        """
        self.users[username] = websocket
        logger.info(f"User {username} joined the session")
        
        # Start game loop if this is the first user
        if len(self.users) == 1:
            self.start_game_loop()

        # Send current game state to the new user
        await self.send_game_state(username)

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
