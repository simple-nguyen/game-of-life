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
        session = websocket_service.get_or_create_session(channel_code)
        await session.add_user(username, websocket)
        
        while True:
            data = await websocket.receive_json()
            await session.handle_message(username, data)
            
    except WebSocketDisconnect:
        logger.info(f"Client disconnected: {username}")
        if session:
            await session.remove_user(username)
            if not session.has_users():
                websocket_service.remove_session(channel_code)
                
    except Exception as e:
        logger.error(f"Error in websocket connection: {str(e)}")
        if session:
            await session.remove_user(username)
            if not session.has_users():
                websocket_service.remove_session(channel_code)
