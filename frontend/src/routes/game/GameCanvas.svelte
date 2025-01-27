<script lang="ts">
    import { onMount } from 'svelte';
    import { wsService, cells } from '$lib/services/websocket';

    let canvas: HTMLCanvasElement;
    let ctx: CanvasRenderingContext2D;
    const cellSize = 20;
    const gridWidth = 50;
    const gridHeight = 30;
    const canvasWidth = gridWidth * cellSize;
    const canvasHeight = gridHeight * cellSize;
    let isDrawing = false;

    onMount(() => {
        ctx = canvas.getContext('2d')!;
        canvas.width = canvasWidth;
        canvas.height = canvasHeight;
        drawGrid();
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

        // Clear canvas
        ctx.clearRect(0, 0, canvasWidth, canvasHeight);
        drawGrid();

        // Draw cells using the store value
        if ($cells) {
            Object.entries($cells).forEach(([key, color]) => {
                const [x, y] = key.split(',').map(Number);
                if (!isNaN(x) && !isNaN(y)) {  
                    ctx.fillStyle = color;
                    ctx.fillRect(x * cellSize + 1, y * cellSize + 1, cellSize - 2, cellSize - 2);
                }
            });
        }
    }

    // More robust reactive statement
    $: if (ctx && $cells) {
        console.log('Cells updated:', Object.keys($cells).length);
        drawCells();
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
        if (!ctx) return;

        const canvas = event.target as HTMLCanvasElement;
        const rect = canvas.getBoundingClientRect();
        const containerElement = canvas.parentElement;

        if (!containerElement) return;

        const viewportX = event.clientX;
        const viewportY = event.clientY;

        const canvasX = viewportX - rect.left;
        const canvasY = viewportY - rect.top;

        const gridX = Math.floor(canvasX / cellSize);
        const gridY = Math.floor(canvasY / cellSize);

        if (gridX >= 0 && gridX < gridWidth && gridY >= 0 && gridY < gridHeight) {
            wsService.placeCell(gridX, gridY);
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
</style>
