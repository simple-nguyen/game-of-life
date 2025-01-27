<script lang="ts">
    import { gameState } from '$lib/services/websocket';

    let isExpanded = true;

    function toggleUserList() {
        isExpanded = !isExpanded;
    }
</script>

<div class="user-list">
    <button class="user-list-header" on:click="{toggleUserList}">
        <h4>Users ({$gameState.users.length})</h4>
        <span class="toggle-icon">{isExpanded ? '▼' : '▶'}</span>
    </button>
    {#if isExpanded}
        <div class="users">
            {#each $gameState.users as user}
                <div class="user-item" class:current="{user.username === $gameState.username}">
                    <span class="user-name">{user.username}</span>
                    <div class="user-color" style="background-color: {user.color};"></div>
                </div>
            {/each}
        </div>
    {/if}
</div>

<style>
    .user-list {
        padding: 1rem;
        background: white;
        padding: 0.5rem;
        border-radius: 0.5rem;
        border: 1px solid gray;
    }

    .user-list-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;
        padding: 0 0.25rem;
        width: 100%;
        background: none;
        border: none;
        text-align: left;
    }

    .user-list-header h4 {
        margin: 0.5rem 0;
        color: black;
    }

    .users {
        margin-top: 0.25rem;
    }

    .user-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem;
        margin: 0.25rem 0;
        border: 1px solid #ddd;
    }

    .user-item.current {
        background: #d7fddd;
    }

    .user-name {
        font-size: 0.9rem;
        color: #666;
    }

    .user-color {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        border: 1px solid #ddd;
    }

    .toggle-icon {
        font-size: 0.8rem;
        color: #666;
    }
</style>
