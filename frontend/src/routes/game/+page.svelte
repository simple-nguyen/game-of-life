`<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { wsService, gameState } from '$lib/services/websocket';
    import GameCanvas from './GameCanvas.svelte';
    import UserList from './UserList.svelte';
    import { goto } from '$app/navigation';

    let username: string;
    let channelCode: string;

    onMount(() => {
        if (!$gameState.channelCode) {
            goto('/login');
        }
        username = $gameState.username || '';
        channelCode = $gameState.channelCode;
    });

    onDestroy(() => {
        wsService.disconnect();
    });
</script>

<div class="game-container">
    <nav class="top-nav">
        <h1>Game of Life</h1>
        <div class="game-info">
            <span>Username: {username}</span>
            <span>Channel: {channelCode}</span>
        </div>
    </nav>

    <div class="game-content">
        <aside class="side-nav">
            <UserList />
        </aside>
        <main class="game-area">
            <GameCanvas />
        </main>
    </div>
</div>

<style>
    .game-container {
        height: 100vh;
        display: flex;
        flex-direction: column;
    }

    .top-nav {
        background-color: #333;
        color: white;
        padding: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .game-info {
        display: flex;
        gap: 1rem;
    }

    .game-content {
        flex: 1;
        display: flex;
        overflow: hidden;
    }

    .side-nav {
        width: 250px;
        background-color: #f5f5f5;
        border-right: 1px solid #ddd;
        overflow-y: auto;
    }

    .game-area {
        flex: 1;
        overflow: hidden;
        padding: 1rem;
    }

    h1 {
        margin: 0;
        font-size: 1.5rem;
    }
</style>`
