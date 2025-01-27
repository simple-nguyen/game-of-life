<script lang="ts">
    import { wsService, gameState } from '$lib/services/websocket';

    interface Pattern {
        name: string;
        description: string;
        cells: [number, number][];
    }

    export const PATTERNS: Pattern[] = [
        {
            name: 'Oscillator',
            description: 'A simple 3-cell pattern that oscillates back and forth',
            cells: [
                [0, 0],
                [1, 0],
                [2, 0]
            ]
        },
        {
            name: 'Toad',
            description: 'A 6-cell pattern that oscillates between two states',
            cells: [
                [1, 1],
                [2, 1],
                [3, 1],
                [0, 2],
                [1, 2],
                [2, 2]
            ]
        },
        {
            name: 'Beacon',
            description: 'A pattern that oscillates between two states by flashing',
            cells: [
                [0, 0],
                [1, 0],
                [0, 1],
                [3, 2],
                [2, 3],
                [3, 3]
            ]
        },
        {
            name: 'Glider',
            description: 'A pattern that moves diagonally across the grid',
            cells: [
                [1, 0],
                [2, 1],
                [0, 2],
                [1, 2],
                [2, 2]
            ]
        },
        {
            name: 'Pulsar',
            description: 'A period 3 oscillator that creates a beautiful symmetric pattern',
            cells: [
                // Top
                [2, 0],
                [3, 0],
                [4, 0],
                [8, 0],
                [9, 0],
                [10, 0],
                // Top sides
                [0, 2],
                [5, 2],
                [7, 2],
                [12, 2],
                [0, 3],
                [5, 3],
                [7, 3],
                [12, 3],
                [0, 4],
                [5, 4],
                [7, 4],
                [12, 4],
                // Middle
                [2, 5],
                [3, 5],
                [4, 5],
                [8, 5],
                [9, 5],
                [10, 5],
                // Bottom middle
                [2, 7],
                [3, 7],
                [4, 7],
                [8, 7],
                [9, 7],
                [10, 7],
                // Bottom sides
                [0, 8],
                [5, 8],
                [7, 8],
                [12, 8],
                [0, 9],
                [5, 9],
                [7, 9],
                [12, 9],
                [0, 10],
                [5, 10],
                [7, 10],
                [12, 10],
                // Bottom
                [2, 12],
                [3, 12],
                [4, 12],
                [8, 12],
                [9, 12],
                [10, 12]
            ]
        },
        {
            name: 'LWSS',
            description: 'Lightweight spaceship that moves horizontally across the grid',
            cells: [
                [0, 0],
                [3, 0],
                [4, 1],
                [0, 2],
                [4, 2],
                [1, 3],
                [2, 3],
                [3, 3],
                [4, 3]
            ]
        }
    ];

    let isExpanded = true;

    function togglePatterns() {
        isExpanded = !isExpanded;
    }

    function selectPattern(pattern: Pattern) {
        // Get random position within grid bounds
        const gridWidth = $gameState.gridWidth;
        const gridHeight = $gameState.gridHeight;
        const patternWidth = Math.max(...pattern.cells.map(([x]) => x)) + 1;
        const patternHeight = Math.max(...pattern.cells.map(([, y]) => y)) + 1;

        // Random position that ensures pattern fits within grid
        const startX = Math.floor(Math.random() * (gridWidth - patternWidth));
        const startY = Math.floor(Math.random() * (gridHeight - patternHeight));

        // Place each cell in the pattern
        pattern.cells.forEach(([x, y]) => {
            wsService.placeCell(startX + x, startY + y);
        });
    }
</script>

<div class="patterns-list">
    <button class="patterns-header" on:click="{togglePatterns}">
        <h4>Patterns</h4>
        <span class="toggle-icon">{isExpanded ? '▼' : '▶'}</span>
    </button>
    {#if isExpanded}
        <div class="patterns">
            {#each PATTERNS as pattern}
                <button class="pattern-item" on:click="{() => selectPattern(pattern)}">
                    <span class="pattern-name">{pattern.name}</span>
                    <span class="pattern-description">{pattern.description}</span>
                </button>
            {/each}
        </div>
    {/if}
</div>

<style>
    .patterns-list {
        padding: 1rem;
        background: white;
        padding: 0.5rem;
        border-radius: 0.5rem;
        border: 1px solid gray;
    }

    .patterns-header {
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

    .patterns-header h4 {
        margin: 0.5rem 0;
        color: black;
    }

    .patterns {
        margin-top: 0.25rem;
    }

    .pattern-item {
        display: flex;
        flex-direction: column;
        padding: 0.5rem;
        margin: 0.25rem 0;
        cursor: pointer;
        border: 1px solid #ddd;
        background: none;
        width: 100%;
        text-align: left;
    }

    .pattern-name,
    .pattern-description {
        font-size: 0.9rem;
        color: #666;
        text-align: center;
    }

    .pattern-description {
        font-size: 0.8rem;
        color: #888;
    }

    .toggle-icon {
        font-size: 0.8rem;
        color: #666;
    }
</style>
