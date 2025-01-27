import { writable } from 'svelte/store';

export interface GameState {
    users: { username: string; color: string }[];
    grid: number[][];
    channelCode: string;
}

export const gameState = writable<GameState>({
    users: [],
    grid: [],
    channelCode: ''
});

class WebSocketService {
    private ws: WebSocket | null = null;

    connect(username: string, channelCode: string): Promise<boolean> {
        return new Promise((resolve) => {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws`;
            
            this.ws = new WebSocket(wsUrl);
            
            this.ws.onopen = () => {
                this.sendMessage({
                    type: 'join',
                    username,
                    channelCode
                });
                resolve(true);
            };

            this.ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                gameState.set(data);
            };

            this.ws.onerror = () => {
                resolve(false);
            };
        });
    }

    sendMessage(message: any) {
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
