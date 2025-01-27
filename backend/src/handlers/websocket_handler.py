import json
import logging
from fastapi import WebSocket, WebSocketDisconnect
from ..services.websocket_service import WebSocketService

logger = logging.getLogger(__name__)

class WebSocketHandler:
    def __init__(self, websocket_service: WebSocketService):
        self.websocket_service = websocket_service

    async def handle_websocket(self, websocket: WebSocket):
        await websocket.accept()
        
        try:
            # Wait for initial join message
            data = await websocket.receive_json()
            if data["type"] != "join":
                await websocket.close()
                return

            username = data["username"]
            channel_code = data.get("channelCode", "")
            websocket_id = str(id(websocket))

            # Get or create session and add user
            session = self.websocket_service.get_or_create_session(channel_code)
            color = self.websocket_service.add_user(session.channel_code, username, websocket_id)

            # Send initial state
            state = self.websocket_service.get_session_state(session.channel_code)
            await websocket.send_json(state)

            # Handle messages
            while True:
                data = await websocket.receive_json()
                
                if data["type"] == "update_cell":
                    x, y = data["x"], data["y"]
                    self.websocket_service.update_cell(session.channel_code, username, x, y)
                    
                    # Broadcast updated state to all users
                    state = self.websocket_service.get_session_state(session.channel_code)
                    await websocket.send_json(state)

        except WebSocketDisconnect:
            logger.info(f"WebSocket disconnected: {websocket_id}")
            if session:
                self.websocket_service.remove_user(session.channel_code, username, websocket_id)
        except Exception as e:
            logger.error(f"WebSocket error: {str(e)}")
            await websocket.close()
