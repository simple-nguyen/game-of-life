from typing import Dict, Set, Tuple
import logging
import random
import string
from .game_session import GameSession

logger = logging.getLogger(__name__)

class WebSocketService:
    def __init__(self):
        """Initialize the WebSocket service."""
        self.sessions: Dict[str, GameSession] = {}
        logger.info("WebSocket service initialized")

    def get_or_create_session(self, channel_code: str) -> Tuple[str, GameSession]:
        """Get an existing session or create a new one.
        
        Args:
            channel_code: Unique identifier for the game session
            
        Returns:
            GameSession: The game session instance
        """
        if channel_code.lower() == "new":
            while True:
                new_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                if new_code not in self.sessions:
                    self.sessions[new_code] = GameSession()
                    return new_code, self.sessions[new_code]
       
        logger.info(self.sessions)

        if channel_code in self.sessions:
            return channel_code, self.sessions[channel_code]
        else:
            raise ValueError("Invalid channel code")

    def remove_session(self, channel_code: str) -> None:
        """Remove a game session.
        
        Args:
            channel_code: Unique identifier for the game session
        """
        if channel_code in self.sessions:
            logger.info(f"Removing game session: {channel_code}")
            self.sessions[channel_code].stop_game_loop()
            del self.sessions[channel_code]