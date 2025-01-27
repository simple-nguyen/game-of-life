from typing import Dict, Set
import logging
import random
from .game_session import GameSession

logger = logging.getLogger(__name__)

COLORS = [
    "#FF0000", "#00FF00", "#0000FF", "#FF00FF", 
    "#00FFFF", "#FFA500", "#800080", "#008000",
    "#FFC0CB", "#FFD700", "#4B0082", "#7B68EE"
]

class WebSocketService:
    def __init__(self):
        """Initialize the WebSocket service."""
        self.sessions: Dict[str, GameSession] = {}
        self.user_sessions: Dict[str, Dict[str, str]] = {}  # channel_code -> {username: color}
        self.user_connections: Dict[str, Set[str]] = {}  # channel_code -> set of websocket connections
        logger.info("WebSocket service initialized")

    def get_or_create_session(self, channel_code: str) -> GameSession:
        """Get an existing session or create a new one.
        
        Args:
            channel_code: Unique identifier for the game session
            
        Returns:
            GameSession: The game session instance
        """
        if not channel_code:
            # Generate a unique channel code if none provided
            while True:
                channel_code = str(random.randint(100000, 999999))
                if channel_code not in self.sessions:
                    break

        if channel_code not in self.sessions:
            logger.info(f"Creating new game session: {channel_code}")
            self.sessions[channel_code] = GameSession()
            self.user_sessions[channel_code] = {}
            self.user_connections[channel_code] = set()
        return self.sessions[channel_code]

    def remove_session(self, channel_code: str) -> None:
        """Remove a game session.
        
        Args:
            channel_code: Unique identifier for the game session
        """
        if channel_code in self.sessions:
            logger.info(f"Removing game session: {channel_code}")
            self.sessions[channel_code].stop_game_loop()
            del self.sessions[channel_code]
            del self.user_sessions[channel_code]
            del self.user_connections[channel_code]

    def get_session(self, channel_code: str) -> GameSession:
        """Get an existing session.
        
        Args:
            channel_code: Unique identifier for the game session
            
        Returns:
            GameSession: The game session instance
            
        Raises:
            KeyError: If session doesn't exist
        """
        if channel_code not in self.sessions:
            raise KeyError(f"Session {channel_code} not found")
        return self.sessions[channel_code]

    def add_user(self, channel_code: str, username: str, websocket_id: str) -> str:
        """Add a user to a session.
        
        Args:
            channel_code: Unique identifier for the game session
            username: Username of the player
            websocket_id: Unique identifier for the websocket connection
            
        Returns:
            str: Assigned color for the user
        """
        if channel_code not in self.user_sessions:
            self.user_sessions[channel_code] = {}
            self.user_connections[channel_code] = set()

        # If username already exists in session, return their color
        if username in self.user_sessions[channel_code]:
            color = self.user_sessions[channel_code][username]
        else:
            # Assign a new color
            used_colors = set(self.user_sessions[channel_code].values())
            available_colors = [c for c in COLORS if c not in used_colors]
            color = available_colors[0] if available_colors else COLORS[0]
            self.user_sessions[channel_code][username] = color

        self.user_connections[channel_code].add(websocket_id)
        return color

    def remove_user(self, channel_code: str, username: str, websocket_id: str) -> None:
        """Remove a user from a session.
        
        Args:
            channel_code: Unique identifier for the game session
            username: Username of the player
            websocket_id: Unique identifier for the websocket connection
        """
        if channel_code in self.user_connections:
            self.user_connections[channel_code].remove(websocket_id)
            
            # Only remove user from session if no more connections from this user
            if not any(conn for conn in self.user_connections[channel_code] 
                      if username in self.user_sessions[channel_code]):
                del self.user_sessions[channel_code][username]

            # Remove session if no more users
            if not self.user_connections[channel_code]:
                self.remove_session(channel_code)

    def get_session_state(self, channel_code: str) -> dict:
        """Get the current state of a session.
        
        Args:
            channel_code: Unique identifier for the game session
            
        Returns:
            dict: Current state including grid and users
        """
        session = self.get_session(channel_code)
        users = [{"username": username, "color": color} 
                for username, color in self.user_sessions[channel_code].items()]
        
        return {
            "grid": session.grid,
            "users": users,
            "channelCode": channel_code
        }

    def update_cell(self, channel_code: str, username: str, x: int, y: int) -> None:
        """Update a cell in the grid.
        
        Args:
            channel_code: Unique identifier for the game session
            username: Username of the player making the update
            x: X coordinate of the cell
            y: Y coordinate of the cell
        """
        session = self.get_session(channel_code)
        color = self.user_sessions[channel_code].get(username)
        if color:
            session.update_cell(x, y, color)
