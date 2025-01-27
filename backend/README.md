# Game of Life Backend

This is the backend service for Conway's Game of Life implementation. It provides a WebSocket-based API for real-time game state updates and multiplayer functionality.

## Features

- Real-time game state management using WebSockets
- Multiplayer support with unique game sessions
- Color-based cell visualization
- Implementation of Conway's Game of Life rules with color inheritance

## Setup

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Run the server:
```bash
python3 -m uvicorn src.main:app --reload
```

The server will start at `http://localhost:8000` by default.

## Development

### Code Style

The project uses several tools to maintain code quality:

- **Black**: Code formatter
  ```bash
  python3 -m black src/ tests/
  ```

- **isort**: Import sorter
  ```bash
  python3 -m isort src/ tests/
  ```

- **flake8**: Linter
  ```bash
  python3 -m flake8 src/ tests/
  ```

### Project Structure

```
backend/
├── src/
│   ├── services/
│   │   ├── game_loop.py      # Core game logic
│   │   ├── game_session.py   # Session management
│   │   └── websocket_service.py  # WebSocket handling
│   └── main.py              # FastAPI application
├── tests/                   # Test files
├── requirements.txt         # Project dependencies
├── pyproject.toml          # Tool configurations
└── .flake8                 # Flake8 configuration
```

## Testing

Run tests using pytest:
```bash
python3 -m pytest
```

## API Documentation

The WebSocket endpoint is available at:
- `/ws/{channel_code}/{username}` - Connect to a game session
  - `channel_code`: Session identifier (use "new" for a new session)
  - `username`: Player identifier

### WebSocket Messages

Messages are JSON-formatted with the following types:

- `cell_update`: Single cell update
- `cell_updates`: Multiple cell updates
- `cell_removals`: Remove cells
- `full_update`: Complete game state
- `channel_code`: Session identifier
- `user_list`: Connected players
