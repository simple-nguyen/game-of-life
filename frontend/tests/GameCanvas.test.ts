import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, fireEvent } from '@testing-library/svelte'
import GameCanvas from '../src/routes/game/GameCanvas.svelte'
import { wsService } from '../src/lib/services/websocket'

vi.mock('../src/lib/services/websocket', () => ({
    wsService: {
        placeCell: vi.fn(),
    },
    cells: {
        subscribe: vi.fn((callback) => {
            callback(new Map())
            return () => {}
        }),
    },
    gameState: {
        subscribe: vi.fn((callback) => {
            callback({
                gridWidth: 50,
                gridHeight: 30,
            })
            return () => {}
        }),
    },
}))

describe('GameCanvas', () => {
    beforeEach(() => {
        vi.clearAllMocks()
    })

    it('renders canvas element', () => {
        const { container } = render(GameCanvas)
        const canvas = container.querySelector('canvas')
        expect(canvas).toBeInTheDocument()
    })

    it('calls placeCell when clicking on canvas', async () => {
        const { container } = render(GameCanvas)
        const canvas = container.querySelector('canvas')
        expect(canvas).toBeInTheDocument()

        // Simulate a click at position (50, 50)
        await fireEvent.mouseDown(canvas!, {
            clientX: 50,
            clientY: 50,
        })

        // Since cellSize is 23, this should translate to grid position (2, 2)
        expect(wsService.placeCell).toHaveBeenCalledWith(2, 2)
    })

    it('handles mouse drag to draw multiple cells', async () => {
        const { container } = render(GameCanvas)
        const canvas = container.querySelector('canvas')
        expect(canvas).toBeInTheDocument()

        // Start drawing
        await fireEvent.mouseDown(canvas!, {
            clientX: 50,
            clientY: 50,
        })

        // Move mouse while drawing
        await fireEvent.mouseMove(canvas!, {
            clientX: 75,
            clientY: 75,
        })

        // Should have called placeCell twice with different coordinates
        expect(wsService.placeCell).toHaveBeenCalledTimes(2)
    })
})
