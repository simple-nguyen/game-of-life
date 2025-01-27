<script lang="ts">
    import { goto } from '$app/navigation';
    import { wsService } from '$lib/services/websocket';

    let username = '';
    let channelCode = '';
    let error = '';

    async function handleSubmit() {
        if (!username.trim()) {
            error = 'Username is required';
            return;
        }

        const connected = await wsService.connect(username, channelCode);
        if (connected) {
            goto('/game');
        } else {
            error = 'Failed to connect to game server';
        }
    }
</script>

<div class="login-container">
    <div class="login-box">
        <h1>Game of Life</h1>
        <form on:submit|preventDefault={handleSubmit}>
            <div class="form-group">
                <label for="username">Username</label>
                <input
                    type="text"
                    id="username"
                    bind:value={username}
                    placeholder="Enter your username"
                />
            </div>
            <div class="form-group">
                <label for="channelCode">Channel Code (optional)</label>
                <input
                    type="text"
                    id="channelCode"
                    bind:value={channelCode}
                    placeholder="Enter channel code or leave empty to create new"
                />
            </div>
            {#if error}
                <div class="error-message">{error}</div>
            {/if}
            <button type="submit">Join Game</button>
        </form>
    </div>
</div>

<style>
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background-color: #f5f5f5;
    }

    .login-box {
        background: white;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 400px;
    }

    h1 {
        text-align: center;
        margin-bottom: 2rem;
        color: #333;
    }

    .form-group {
        margin-bottom: 1rem;
    }

    label {
        display: block;
        margin-bottom: 0.5rem;
        color: #666;
    }

    input {
        width: 100%;
        padding: 0.5rem;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 1rem;
    }

    button {
        width: 100%;
        padding: 0.75rem;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        font-size: 1rem;
        cursor: pointer;
        margin-top: 1rem;
    }

    button:hover {
        background-color: #45a049;
    }

    .error-message {
        color: #ff4444;
        margin-top: 0.5rem;
        text-align: center;
    }
</style>
