<script lang="ts">
    import { page } from '$app/stores';
</script>

<div class="error-container">
    <h1>{$page.status}: {$page.error?.message}</h1>
    <a href="/">Go back home</a>
</div>

<style>
    .error-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        text-align: center;
        padding: 1rem;
    }

    h1 {
        color: var(--text-color);
        margin-bottom: 1rem;
    }

    a {
        color: var(--primary-color);
        text-decoration: none;
        font-size: 1.1rem;
    }

    a:hover {
        text-decoration: underline;
    }
</style>
