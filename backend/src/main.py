from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv

from .services.websocket_service import WebSocketService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize WebSocket service
websocket_service = WebSocketService()

@app.websocket("/ws/{channel_code}/{username}")
async def websocket_endpoint(websocket: WebSocket, channel_code: str, username: str):
    session = None
    try:
        await websocket.accept()

        logger.info(f"User {username} connecting to channel {channel_code}")
        
        channel_code, session = websocket_service.get_or_create_session(channel_code)
        logger.info(f"Session - channel: {channel_code}")
        
        if username in session.users:
            logger.error(f"Username {username} already taken in channel {channel_code}")
            await websocket.send_json({
                "type": "error",
                "message": "Username already taken"
            })
            await websocket.close()
            return
        
        user_colors = await session.add_user(username, websocket)

        if channel_code != "new":
            logger.info(f"Sending new channel code {channel_code} to {username}")
            await websocket.send_json({
                "type": "channel_code",
                "code": channel_code
            })
        
        await session.broadcast({
            "type": "user_list",
            "users": user_colors
        })

        while True:
            data = await websocket.receive_json()
            logger.info(f"Received message from {username}: {data}")    
            await session.handle_message(username, data)
            
    except WebSocketDisconnect:
        logger.info(f"Client disconnected: {username}")
        if session:
            await session.remove_user(username)

            remaining_users = list(session.users.keys())
            await session.broadcast({
                "type": "user_list",
                "users": [{"username": user, "color": session.user_colors[user]} for user in remaining_users]
            })

            if not remaining_users:
                websocket_service.remove_session(channel_code)
                logger.info(f"Removed empty session {channel_code}")
     
    except Exception as e:
        logger.error(f"Error in websocket connection: {str(e)}")
        if session:
            await session.remove_user(username)
            if not session.has_users():
                websocket_service.remove_session(channel_code)
    finally:
        try:
            await websocket.close()
        except Exception as e:
            logger.error(f"Error closing websocket: {str(e)}")