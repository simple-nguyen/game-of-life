import { writable } from 'svelte/store';

export interface GameState {
    users: { username: string; color: string }[];
    grid: number[][];
    channelCode: string;
    username: string;
}

export const gameState = writable<GameState>({
    users: [],
    grid: [],
    channelCode: '',
    username: '',
});

class WebSocketService {
    private ws: WebSocket | null = null;

    connect(username: string, channelCode: string): Promise<string> {
        return new Promise((resolve) => {
            const backendUrl = import.meta.env.VITE_BACKEND_WS_URL || 'ws://localhost:8000';
            const wsUrl = `${backendUrl}/ws/${channelCode || "new"}/${username}`;
            
            this.ws = new WebSocket(wsUrl);
            
            this.ws.onopen = async () => {
                gameState.update(state => ({ ...state, username }));
            };

            this.ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                switch (data.type) {
                    case 'game_state':
                        gameState.update(state => {
                            const newState = { ...state, grid: data.state };
                            return newState;
                        });
                        break;
                    case 'channel_code':
                        const code = data.code;
                        gameState.update(state => {
                            const newState = { ...state, channelCode: code };
                            return newState;
                        });
                        resolve(code);
                        break;
                    case 'user_list':
                        gameState.update(state => {
                            const newState = { ...state, users: data.users };
                            return newState;
                        });
                        break;
                }
            };

            this.ws.onerror = () => {
                resolve('');  // Resolve with empty string on error
            };
        });
    }

    private sendMessage(message: any) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(message));
        }
    }

    updateCell(x: number, y: number) {
        this.sendMessage({
            type: 'update_cell',
            x,
            y
        });
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
}

export const wsService = new WebSocketService();
