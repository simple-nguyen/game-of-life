`<script lang="ts">
    import { gameState } from '$lib/services/websocket';
</script>

<div class="user-list">
    <h2>Connected Users</h2>
    <div class="users">
        {#each $gameState.users as user}
            <div class="user-item">
                <div class="user-color" style="background-color: {user.color}"></div>
                <span class="user-name">{user.username}</span>
            </div>
        {/each}
    </div>
</div>

<style>
    .user-list {
        padding: 1rem;
    }

    h2 {
        margin: 0 0 1rem 0;
        font-size: 1.2rem;
        color: #333;
    }

    .users {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .user-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem;
        background-color: white;
        border-radius: 4px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }

    .user-color {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        border: 1px solid #ddd;
    }

    .user-name {
        font-size: 0.9rem;
        color: #666;
    }
</style>`
