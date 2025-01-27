import logging
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

logger = logging.getLogger(__name__)


@dataclass
class CellUpdate:
    x: int
    y: int
    color: str


@dataclass
class CellRemoval:
    x: int
    y: int


def _normalize_color(color: str) -> str:
    return color.upper() if color else color


def _average_colors(colors: List[str]) -> str:
    """Calculate the average of multiple hex colors.

    Args:
        colors: List of hex color strings (e.g., ['#FF0000', '#00FF00'])

    Returns:
        Averaged color as hex string
    """
    if not colors:
        return "#000000"

    # Convert hex to RGB values
    rgb_values = []
    for color in colors:
        # Remove '#' and convert to RGB
        color = color.lstrip("#")
        rgb = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))
        rgb_values.append(rgb)

    # Calculate average for each channel
    avg_r = sum(rgb[0] for rgb in rgb_values) // len(rgb_values)
    avg_g = sum(rgb[1] for rgb in rgb_values) // len(rgb_values)
    avg_b = sum(rgb[2] for rgb in rgb_values) // len(rgb_values)

    # Convert back to hex
    return f"#{avg_r:02x}{avg_g:02x}{avg_b:02x}"


class GameLoop:
    def __init__(self, width: int = 50, height: int = 30):
        """Initialize the game loop.

        Args:
            width: Width of the game board
            height: Height of the game board
        """
        self.width = width
        self.height = height
        self.cells: Dict[Tuple[int, int], str] = {}  # (x, y) -> color
        logger.info(f"Game loop initialized with dimensions {width}x{height}")

    def is_within_grid(self, x: int, y: int) -> bool:
        """Check if coordinates are within grid bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def place_cell(self, x: int, y: int, color: str) -> None:
        """Place a cell on the board.

        Args:
            x: X coordinate
            y: Y coordinate
            color: Color of the cell
        """
        if self.is_within_grid(x, y):
            logger.info(f"Placing cell at ({x}, {y}) with color {color}")
            self.cells[(x, y)] = _normalize_color(color)
        else:
            logger.warning(f"Attempted to place cell outside grid at ({x}, {y})")

    def remove_cell(self, x: int, y: int) -> None:
        """Remove a cell from the board.

        Args:
            x: X coordinate
            y: Y coordinate
        """
        if (x, y) in self.cells:
            logger.info(f"Removing cell at ({x}, {y})")
            del self.cells[(x, y)]

    def get_state(self) -> List[Dict[str, str]]:
        """Get the current state of the game.

        Returns:
            List of dictionaries containing cell positions and colors
        """
        return [
            {"x": x, "y": y, "color": _normalize_color(color)}
            for (x, y), color in self.cells.items()
        ]

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
                if self.is_within_grid(new_x, new_y):
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
            List of colors of neighboring cells
        """
        return [
            self.cells[(nx, ny)]
            for nx, ny in self._get_neighbors(x, y)
            if (nx, ny) in self.cells
        ]

    def next_generation(self) -> Dict[Tuple[int, int], str]:
        """Calculate the next generation of cells."""
        # Get all cells to check (live cells and their neighbors)
        cells_to_check: Set[Tuple[int, int]] = set()

        # Only check cells that are within the grid
        for x, y in self.cells.keys():
            if self.is_within_grid(x, y):
                cells_to_check.add((x, y))
                # Only add neighbors that are within the grid
                for nx, ny in self._get_neighbors(x, y):
                    if self.is_within_grid(nx, ny):
                        cells_to_check.add((nx, ny))

        new_cells: Dict[Tuple[int, int], str] = {}

        # Check each cell
        for x, y in cells_to_check:
            # Since we filtered above, all cells here are within grid
            live_neighbors = self._count_live_neighbors(x, y)
            is_alive = (x, y) in self.cells

            # Apply Conway's Game of Life rules
            if is_alive and live_neighbors in [2, 3]:
                # Cell survives
                new_cells[(x, y)] = self.cells[(x, y)]
            elif not is_alive and live_neighbors == 3:
                # Cell is born
                neighbor_colors = self._get_neighbor_colors(x, y)
                if neighbor_colors:
                    new_cells[(x, y)] = _average_colors(neighbor_colors)

        return new_cells

    def update_game_state(self) -> tuple[list[CellUpdate], list[CellRemoval]]:
        """Update the game state and return lists of updates and removals."""
        new_state = self.next_generation()

        # Find cells that have changed
        updates = []
        removals = []

        # Check for new or modified cells
        for pos, color in new_state.items():
            if pos not in self.cells or self.cells[pos] != color:
                if color != "#000000":  # Only send live cells
                    updates.append(CellUpdate(pos[0], pos[1], _normalize_color(color)))
                elif self.cells.get(pos, "#000000") != "#000000":  # Cell died
                    removals.append(CellRemoval(pos[0], pos[1]))

        # Check for removed cells (cells that were alive but are now dead)
        for pos, old_color in self.cells.items():
            if old_color != "#000000" and (
                pos not in new_state or new_state[pos] == "#000000"
            ):
                removals.append(CellRemoval(pos[0], pos[1]))

        # Update game state
        self.cells = new_state

        return updates, removals
