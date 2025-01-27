from typing import Dict
import logging
from .game_session import GameSession

logger = logging.getLogger(__name__)

class WebSocketService:
    def __init__(self):
        """Initialize the WebSocket service."""
        self.sessions: Dict[str, GameSession] = {}
        logger.info("WebSocket service initialized")

    def get_or_create_session(self, channel_code: str) -> GameSession:
        """Get an existing session or create a new one.
        
        Args:
            channel_code: Unique identifier for the game session
            
        Returns:
            GameSession: The game session instance
        """
        if channel_code not in self.sessions:
            logger.info(f"Creating new game session: {channel_code}")
            self.sessions[channel_code] = GameSession()
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
