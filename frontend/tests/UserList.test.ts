import { describe, it, expect, vi } from 'vitest'
import { render, fireEvent } from '@testing-library/svelte'
import UserList from '../src/routes/game/UserList.svelte'

vi.mock('../src/lib/services/websocket', () => ({
    gameState: {
        subscribe: vi.fn((callback) => {
            callback({
                users: [
                    { username: 'user1', color: '#FF0000' },
                    { username: 'user2', color: '#00FF00' },
                ],
                username: 'user1',
            })
            return () => {}
        }),
    },
}))

describe('UserList', () => {
    it('renders user list with correct number of users', () => {
        const { container } = render(UserList)
        const header = container.querySelector('.user-list-header h4')
        expect(header).toHaveTextContent('Users (2)')
    })

    it('shows all users when expanded', () => {
        const { container } = render(UserList)
        const userItems = container.querySelectorAll('.user-item')
        expect(userItems[0]).toHaveTextContent('user1')
        expect(userItems[1]).toHaveTextContent('user2')
        expect(container.querySelector('.toggle-icon')).toHaveTextContent('▼') // Expanded by default
    })

    it('toggles user list visibility when clicking header', async () => {
        const { container } = render(UserList)
        const header = container.querySelector('.user-list-header')
        expect(header).not.toBeNull()

        // List is expanded by default, user1 should be visible
        const user1Element = container.querySelector('.user-item')
        expect(user1Element).toHaveTextContent('user1')

        // Click to collapse
        await fireEvent.click(header!)
        expect(container.querySelector('.users')).toBeNull()
        expect(container.querySelector('.toggle-icon')).toHaveTextContent('▶')

        // Click to expand
        await fireEvent.click(header!)
        expect(container.querySelector('.users')).toBeInTheDocument()
        expect(container.querySelector('.toggle-icon')).toHaveTextContent('▼')
    })

    it('highlights current user', () => {
        const { container } = render(UserList)
        const userItems = container.querySelectorAll('.user-item')
        expect(userItems[0]).toHaveClass('current') // user1 is current
        expect(userItems[1]).not.toHaveClass('current') // user2 is not current
    })
})
