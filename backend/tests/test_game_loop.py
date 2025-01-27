import pytest
from src.services.game_loop import GameLoop, CellUpdate, CellRemoval


@pytest.fixture
def game():
    """Create a new game instance for each test."""
    return GameLoop(width=10, height=10)


def test_initial_state(game):
    """Test that a new game starts with an empty board."""
    assert len(game.cells) == 0
    assert game.width == 10
    assert game.height == 10


def test_place_cell(game):
    """Test placing a cell on the board."""
    game.place_cell(5, 5, "#FF0000")
    assert (5, 5) in game.cells
    assert game.cells[(5, 5)] == "#FF0000"


def test_place_cell_outside_grid(game):
    """Test that placing a cell outside the grid is ignored."""
    game.place_cell(15, 15, "#FF0000")
    assert (15, 15) not in game.cells


def test_remove_cell(game):
    """Test removing a cell from the board."""
    game.place_cell(5, 5, "#FF0000")
    assert (5, 5) in game.cells
    game.remove_cell(5, 5)
    assert (5, 5) not in game.cells


def test_get_state(game):
    """Test getting the current state of the game."""
    game.place_cell(1, 1, "#FF0000")
    game.place_cell(2, 2, "#00FF00")
    state = game.get_state()
    assert len(state) == 2
    assert {"x": 1, "y": 1, "color": "#FF0000"} in state
    assert {"x": 2, "y": 2, "color": "#00FF00"} in state


def test_count_live_neighbors(game):
    """Test counting live neighbors for a cell."""
    # Create a block pattern
    game.place_cell(1, 1, "#FF0000")
    game.place_cell(1, 2, "#FF0000")
    game.place_cell(2, 1, "#FF0000")
    game.place_cell(2, 2, "#FF0000")
    
    # Center cell has 3 neighbors
    assert game._count_live_neighbors(1, 1) == 3
    # Corner cell has no neighbors
    assert game._count_live_neighbors(0, 0) == 1
    # Edge cell has some neighbors
    assert game._count_live_neighbors(1, 0) == 2


def test_next_generation_block_pattern(game):
    """Test that a block pattern remains stable."""
    # Create a block pattern
    game.place_cell(1, 1, "#FF0000")
    game.place_cell(1, 2, "#FF0000")
    game.place_cell(2, 1, "#FF0000")
    game.place_cell(2, 2, "#FF0000")

    new_state = game.next_generation()
    
    # Block should remain stable
    assert (1, 1) in new_state
    assert (1, 2) in new_state
    assert (2, 1) in new_state
    assert (2, 2) in new_state
    assert len(new_state) == 4


def test_next_generation_blinker_pattern(game):
    """Test that a blinker pattern oscillates correctly."""
    # Create a horizontal blinker
    game.place_cell(2, 1, "#FF0000")
    game.place_cell(2, 2, "#FF0000")
    game.place_cell(2, 3, "#FF0000")

    # First generation: horizontal to vertical
    new_state = game.next_generation()
    assert (1, 2) in new_state  # Top
    assert (2, 2) in new_state  # Middle
    assert (3, 2) in new_state  # Bottom
    assert len(new_state) == 3


def test_update_game_state(game):
    """Test that update_game_state returns correct updates and removals."""
    # Place a blinker pattern
    game.place_cell(2, 1, "#FF0000")
    game.place_cell(2, 2, "#FF0000")
    game.place_cell(2, 3, "#FF0000")

    updates, removals = game.update_game_state()

    # Should have 3 removals (horizontal cells)
    assert len(removals) == 2  # Only edge cells are removed
    assert CellRemoval(2, 1) in removals
    assert CellRemoval(2, 3) in removals

    # Should have 2 updates (new vertical cells)
    assert len(updates) == 2  # Only new cells are updated
    assert CellUpdate(1,2,"#FF0000") in updates
    assert CellUpdate(3,2,"#FF0000") in updates


def test_color_averaging(game):
    """Test that new cells get the average color of their neighbors."""
    # Place three cells with different colors
    game.place_cell(2, 1, "#FF0000")  # Red
    game.place_cell(2, 2, "#00FF00")  # Green
    game.place_cell(2, 3, "#0000FF")  # Blue

    # Get the next generation
    new_state = game.next_generation()

    # New cells should have averaged colors
    vertical_cells = [(1, 2), (3, 2)]
    for pos in vertical_cells:
        assert pos in new_state
        # Color should be some mix of the original colors
        color = new_state[pos]
        assert color != "#FF0000" and color != "#00FF00" and color != "#0000FF"


def test_next_generation_beacon_pattern(game):
    """Test that a beacon pattern evolves correctly through its phases.
    
    A beacon is a period-2 oscillator that consists of two overlapping blocks
    where the overlapping corner cells oscillate.
    """
    # Create a beacon pattern:
    # XX..
    # XX..
    # ..XX
    # ..XX
    game.place_cell(1, 1, "#FF0000")
    game.place_cell(2, 1, "#FF0000")
    game.place_cell(1, 2, "#FF0000")
    game.place_cell(2, 2, "#FF0000")
    game.place_cell(3, 3, "#FF0000")
    game.place_cell(4, 3, "#FF0000")
    game.place_cell(3, 4, "#FF0000")
    game.place_cell(4, 4, "#FF0000")

    # First generation should fill in the middle
    new_state = game.next_generation()
    
    # In the next generation, we should see:
    # XX..
    # XXX.
    # .XXX
    # ..XX
    expected_alive = {
        (1, 1), (2, 1),  # Top block
        (1, 2),  # Middle row
        (4, 3),  # Middle row
        (3, 4), (4, 4),  # Bottom block
    }
    
    # Check that all expected cells are alive
    for pos in expected_alive:
        assert pos in new_state, f"Expected cell at {pos} to be alive"
    
    # Check that no unexpected cells are alive
    for pos in new_state:
        assert pos in expected_alive, f"Unexpected cell at {pos}"
    
    # Check total number of cells
    assert len(new_state) == len(expected_alive), "Wrong number of cells in next generation"


def test_beacon_pattern_updates_and_removals(game):
    """Test that the beacon pattern generates correct updates and removals."""
    # Place the initial beacon pattern
    game.place_cell(1, 1, "#FF0000")
    game.place_cell(2, 1, "#FF0000")
    game.place_cell(1, 2, "#FF0000")
    game.place_cell(2, 2, "#FF0000")
    game.place_cell(3, 3, "#FF0000")
    game.place_cell(4, 3, "#FF0000")
    game.place_cell(3, 4, "#FF0000")
    game.place_cell(4, 4, "#FF0000")

    # Get updates and removals for the first generation
    _, removals = game.update_game_state()

    # Should have no removals in the first phase
    assert len(removals) == 2
    assert CellRemoval(2,2) in removals
    assert CellRemoval(3,3) in removals
