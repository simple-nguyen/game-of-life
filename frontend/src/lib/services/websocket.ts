import { writable, get } from 'svelte/store';

export interface GameState {
    users: { username: string; color: string }[];
    channelCode: string;
    username: string;
    gridWidth: number;
    gridHeight: number;
}

export interface Cell extends Record<string, string> {}

export const gameState = writable<GameState>({
    users: [],
    channelCode: '',
    username: '',
    gridWidth: 50,
    gridHeight: 30
});

export const cells = writable<Cell>({});

interface CellData {
    x: string;
    y: string;
    color: string;
}

interface WebSocketMessage {
    type: string;
    [key: string]: unknown;
}

class WebSocketService {
    private ws: WebSocket | null = null;

    connect(username: string, channelCode: string): Promise<string> {
        return new Promise((resolve) => {
            const backendUrl = import.meta.env.VITE_BACKEND_WS_URL || 'ws://localhost:8000';
            const wsUrl = `${backendUrl}/ws/${channelCode || 'new'}/${username}`;

            this.ws = new WebSocket(wsUrl);

            this.ws.onopen = async () => {
                gameState.update((state) => ({ ...state, username }));
            };

            this.ws.onmessage = (event) => {
                const data: WebSocketMessage = JSON.parse(event.data);
                switch (data.type) {
                    case 'cell_updates': {
                        cells.update((state) => {
                            const newState = { ...state };
                            data.updates.forEach(({ x, y, color }: CellData) => {
                                newState[`${x},${y}`] = color;
                            });
                            return newState;
                        });
                        break;
                    }
                    case 'cell_removals': {
                        cells.update((state) => {
                            const newState = { ...state };
                            data.removals.forEach(({ x, y }: CellData) => {
                                delete newState[`${x},${y}`];
                            });
                            return newState;
                        });
                        break;
                    }
                    case 'cell_update':
                        cells.update((state) => {
                            const newState = { ...state, [`${data.x},${data.y}`]: data.color };
                            return newState;
                        });
                        break;
                    case 'full_update':
                        const newState: Cell = {};
                        data.state.forEach(({ x, y, color }: CellData) => {
                            newState[`${x},${y}`] = color;
                        });
                        cells.set(newState);
                        break;
                    case 'channel_code':
                        const code = data.code;
                        if (code) {
                            gameState.update((state) => {
                                const newState = { ...state, channelCode: code };
                                return newState;
                            });
                            resolve(code);
                        }
                        break;
                    case 'user_list':
                        gameState.update((state) => {
                            const newState = { ...state, users: data.users };
                            return newState;
                        });
                        break;
                }
            };

            this.ws.onerror = () => {
                resolve(''); // Resolve with empty string on error
            };
        });
    }

    sendMessage(message: WebSocketMessage): void {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(message));
        }
    }

    placeCell(x: number, y: number): void {
        const currentGameState = get(gameState);
        this.sendMessage({
            type: 'place_cell',
            x,
            y,
            color: currentGameState.users.find((u) => u.username === currentGameState.username)
                ?.color
        });
    }

    disconnect(): void {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }
}

export const wsService = new WebSocketService();
