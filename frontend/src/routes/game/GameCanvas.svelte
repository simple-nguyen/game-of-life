<script lang="ts">
    import { onMount } from 'svelte';
    import { wsService, cells, gameState } from '$lib/services/websocket';

    let canvas: HTMLCanvasElement;
    let ctx: CanvasRenderingContext2D;
    const cellSize = 23;
    let gridWidth = $gameState.gridWidth;
    let gridHeight = $gameState.gridHeight;
    let canvasWidth: number;
    let canvasHeight: number;
    let isDrawing = false;

    function updateCanvasDimensions() {
        canvasWidth = gridWidth * cellSize;
        canvasHeight = gridHeight * cellSize;
        if (canvas) {
            canvas.width = canvasWidth;
            canvas.height = canvasHeight;
            drawGrid();
            drawCells();
        }
    }

    onMount(() => {
        ctx = canvas.getContext('2d')!;
        updateCanvasDimensions();
    });

    function drawGrid() {
        if (!ctx) return;

        ctx.strokeStyle = '#ddd';
        ctx.lineWidth = 1;

        // Draw vertical lines
        for (let x = 0; x <= canvasWidth; x += cellSize) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvasHeight);
            ctx.stroke();
        }

        // Draw horizontal lines
        for (let y = 0; y <= canvasHeight; y += cellSize) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(canvasWidth, y);
            ctx.stroke();
        }
    }

    function drawCells() {
        if (!ctx) return;

        // Clear previous cells
        ctx.clearRect(0, 0, canvasWidth, canvasHeight);
        drawGrid();

        // Draw current cells
        for (const [key, color] of Object.entries($cells)) {
            const [x, y] = key.split(',').map(Number);
            if (x >= 0 && x < gridWidth && y >= 0 && y < gridHeight) {
                ctx.fillStyle = color;
                ctx.fillRect(x * cellSize + 1, y * cellSize + 1, cellSize - 1, cellSize - 1);
            }
        }
    }

    // More robust reactive statement
    $: if (ctx && $cells) {
        drawCells();
    }
    $: if ($gameState.gridWidth && $gameState.gridHeight) {
        gridWidth = $gameState.gridWidth;
        gridHeight = $gameState.gridHeight;
        updateCanvasDimensions();
    }

    function handleMouseDown(event: MouseEvent) {
        isDrawing = true;
        handleDraw(event);
    }

    function handleMouseMove(event: MouseEvent) {
        if (isDrawing) {
            handleDraw(event);
        }
    }

    function handleMouseUp() {
        isDrawing = false;
    }

    function handleDraw(event: MouseEvent) {
        const rect = canvas.getBoundingClientRect();
        const x = Math.floor((event.clientX - rect.left) / cellSize);
        const y = Math.floor((event.clientY - rect.top) / cellSize);

        if (x >= 0 && x < gridWidth && y >= 0 && y < gridHeight) {
            wsService.placeCell(x, y);
        }
    }
</script>

<canvas
    bind:this="{canvas}"
    on:mousedown="{handleMouseDown}"
    on:mousemove="{handleMouseMove}"
    on:mouseup="{handleMouseUp}"
    on:mouseleave="{handleMouseUp}"
></canvas>

<style>
    canvas {
        display: block;
        background-color: white;
        cursor: pointer;
        margin: auto 1.2rem;
    }
</style>
