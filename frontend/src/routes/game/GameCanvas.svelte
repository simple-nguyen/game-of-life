`<script lang="ts">
    import { onMount } from 'svelte';
    import { wsService, gameState } from '$lib/services/websocket';

    let canvas: HTMLCanvasElement;
    let ctx: CanvasRenderingContext2D;
    let cellSize = 20;
    let isDrawing = false;

    $: if (canvas && $gameState.grid) {
        drawGrid();
    }

    onMount(() => {
        ctx = canvas.getContext('2d')!;
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        return () => {
            window.removeEventListener('resize', resizeCanvas);
        };
    });

    function resizeCanvas() {
        const container = canvas.parentElement!;
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight;
        drawGrid();
    }

    function drawGrid() {
        if (!ctx) return;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const rows = $gameState.grid.length;
        const cols = $gameState.grid[0]?.length || 0;

        // Draw cells
        for (let y = 0; y < rows; y++) {
            for (let x = 0; x < cols; x++) {
                const cellValue = $gameState.grid[y][x];
                if (cellValue) {
                    const user = $gameState.users.find(u => u.color === cellValue);
                    if (user) {
                        ctx.fillStyle = user.color;
                        ctx.fillRect(x * cellSize, y * cellSize, cellSize - 1, cellSize - 1);
                    }
                }
            }
        }

        // Draw grid lines
        ctx.strokeStyle = '#ddd';
        ctx.beginPath();
        for (let x = 0; x <= cols; x++) {
            ctx.moveTo(x * cellSize, 0);
            ctx.lineTo(x * cellSize, rows * cellSize);
        }
        for (let y = 0; y <= rows; y++) {
            ctx.moveTo(0, y * cellSize);
            ctx.lineTo(cols * cellSize, y * cellSize);
        }
        ctx.stroke();
    }

    function handleMouseDown(e: MouseEvent) {
        isDrawing = true;
        updateCell(e);
    }

    function handleMouseMove(e: MouseEvent) {
        if (isDrawing) {
            updateCell(e);
        }
    }

    function handleMouseUp() {
        isDrawing = false;
    }

    function updateCell(e: MouseEvent) {
        const rect = canvas.getBoundingClientRect();
        const x = Math.floor((e.clientX - rect.left) / cellSize);
        const y = Math.floor((e.clientY - rect.top) / cellSize);

        if (x >= 0 && x < $gameState.grid[0].length && y >= 0 && y < $gameState.grid.length) {
            wsService.updateCell(x, y);
        }
    }
</script>

<canvas
    bind:this={canvas}
    on:mousedown={handleMouseDown}
    on:mousemove={handleMouseMove}
    on:mouseup={handleMouseUp}
    on:mouseleave={handleMouseUp}
></canvas>

<style>
    canvas {
        display: block;
        background-color: white;
        cursor: pointer;
    }
</style>`
