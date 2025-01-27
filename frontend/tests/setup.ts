import * as matchers from '@testing-library/jest-dom/matchers'
import { expect, vi } from 'vitest'

expect.extend(matchers)

// Mock ResizeObserver
global.ResizeObserver = vi.fn().mockImplementation(() => ({
    observe: vi.fn(),
    unobserve: vi.fn(),
    disconnect: vi.fn(),
}))

// Mock Canvas
HTMLCanvasElement.prototype.getContext = vi.fn().mockReturnValue({
    clearRect: vi.fn(),
    beginPath: vi.fn(),
    moveTo: vi.fn(),
    lineTo: vi.fn(),
    stroke: vi.fn(),
    fillRect: vi.fn(),
})
