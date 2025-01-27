from typing import Dict, List, Tuple, Set
import logging
import random

logger = logging.getLogger(__name__)

class GameLoop:
    def __init__(self, width: int = 50, height: int = 30):
        """Initialize the game loop.
        
        Args:
            width: Width of the game board
            height: Height of the game board
        """
        self.width = width
        self.height = height
        self.cells: Dict[Tuple[int, int], str] = {}  # (x, y) -> username
        logger.info(f"Game loop initialized with dimensions {width}x{height}")

    def place_cell(self, x: int, y: int, username: str) -> None:
        """Place a cell on the board.
        
        Args:
            x: X coordinate
            y: Y coordinate
            username: User who placed the cell
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[(x, y)] = username
            logger.debug(f"Cell placed at ({x}, {y}) by {username}")

    def remove_cell(self, x: int, y: int) -> None:
        """Remove a cell from the board.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.cells.pop((x, y), None)

    def get_state(self) -> List[dict]:
        """Get the current state of the game.
        
        Returns:
            List of dictionaries containing cell positions and colors
        """
        return [{"x": x, "y": y, "username": username} 
                for (x, y), username in self.cells.items()]

    def _get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get all neighboring cells for a position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            List of (x, y) tuples for neighboring positions
        """
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.width and 0 <= new_y < self.height:
                    neighbors.append((new_x, new_y))
        return neighbors

    def _count_live_neighbors(self, x: int, y: int) -> int:
        """Count the number of live neighbors for a cell.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Number of live neighboring cells
        """
        return sum(1 for nx, ny in self._get_neighbors(x, y) if (nx, ny) in self.cells)

    def _get_neighbor_colors(self, x: int, y: int) -> List[str]:
        """Get the colors of all live neighboring cells.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            List of usernames (colors) of neighboring cells
        """
        return [self.cells[(nx, ny)] 
                for nx, ny in self._get_neighbors(x, y) 
                if (nx, ny) in self.cells]

    def next_generation(self) -> None:
        """Calculate the next generation of cells."""
        # Get all cells to check (live cells and their neighbors)
        cells_to_check: Set[Tuple[int, int]] = set()
        for x, y in list(self.cells.keys()):
            cells_to_check.add((x, y))
            cells_to_check.update(self._get_neighbors(x, y))

        new_cells: Dict[Tuple[int, int], str] = {}
        
        # Check each cell
        for x, y in cells_to_check:
            live_neighbors = self._count_live_neighbors(x, y)
            is_alive = (x, y) in self.cells

            # Apply Conway's Game of Life rules
            if is_alive and live_neighbors in [2, 3]:
                # Cell survives
                new_cells[(x, y)] = self.cells[(x, y)]
            elif not is_alive and live_neighbors == 3:
                # Cell is born
                neighbor_colors = self._get_neighbor_colors(x, y)
                # New cell gets a random color from its parents
                new_cells[(x, y)] = random.choice(neighbor_colors)

        self.cells = new_cells
