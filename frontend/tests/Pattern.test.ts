import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, fireEvent } from '@testing-library/svelte'
import Pattern from '../src/routes/game/Pattern.svelte'
import { wsService } from '../src/lib/services/websocket'

vi.mock('../src/lib/services/websocket', () => ({
    wsService: {
        placeCell: vi.fn(),
    },
    gameState: {
        subscribe: vi.fn((callback) => {
            callback({
                gridWidth: 50,
                gridHeight: 30,
                selectedPattern: 'beacon',
            })
            return () => {}
        }),
    },
}))

describe('Pattern', () => {
    beforeEach(() => {
        vi.clearAllMocks()
    })

    it('renders pattern selector', () => {
        const { container } = render(Pattern)
        const header = container.querySelector('.patterns-header h4')
        expect(header).toHaveTextContent('Patterns')
        expect(container.querySelector('.pattern-name')).toHaveTextContent('Oscillator')
    })

    it('places pattern when clicking pattern button', async () => {
        const { container } = render(Pattern)
        
        // Click beacon pattern
        const beaconButton = Array.from(container.querySelectorAll('.pattern-name'))
            .find(el => el.textContent === 'Beacon')
            ?.closest('button')
        expect(beaconButton).not.toBeNull()
        await fireEvent.click(beaconButton!)

        // Should have called placeCell multiple times for the pattern
        expect(wsService.placeCell).toHaveBeenCalled()
        // Beacon pattern has 6 cells, so placeCell should be called 6 times
        expect(wsService.placeCell).toHaveBeenCalledTimes(6)
    })

    it('toggles pattern list when clicking header', async () => {
        const { container } = render(Pattern)
        const header = container.querySelector('.patterns-header')
        expect(header).not.toBeNull()

        // List is expanded by default
        expect(container.querySelector('.patterns')).toBeInTheDocument()
        expect(container.querySelector('.toggle-icon')).toHaveTextContent('▼')

        // Click to collapse
        await fireEvent.click(header!)
        expect(container.querySelector('.patterns')).not.toBeInTheDocument()
        expect(container.querySelector('.toggle-icon')).toHaveTextContent('▶')

        // Click to expand
        await fireEvent.click(header!)
        expect(container.querySelector('.patterns')).toBeInTheDocument()
        expect(container.querySelector('.toggle-icon')).toHaveTextContent('▼')
    })
})
