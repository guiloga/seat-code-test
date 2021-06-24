import numpy as np
from typing import Tuple

from .values import Point, Cardinal


class Mower:
    def __init__(self, position: Point, orientation: Cardinal):
        self._position = position
        self._orientation = orientation
        
        self._initial_position = position

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, position: Point):
        self._position = position

    @property
    def orientation(self):
        return self._orientation
    
    @orientation.setter
    def orientation(self, orientation: Cardinal):
        self._orientation = orientation
    
    @property
    def initial_position(self):
        return self._initial_position


class Palete:
    def __init__(self, dimension: Tuple[int, int]):
        self._rows, self._cols = dimension
        self._build_grid(*dimension)

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @property
    def grid(self) -> np.array:
        return self._grid

    def _build_grid(self, rows: int, cols: int) -> np.array:
        coords = [
            list(range(rows + 1)),
            list(range(cols + 1))
        ]
        self._grid = np.array(coords, ndmin=2)

    def is_outside(self, point: Point):
        for i in self._grid[0]:
            for j in self._grid[1]:
                if (i, j) == point.coords:
                    return False
        return True

    def draw_grid(self, side: int = 3, mower: Mower = None, ):
        # TODO: refactor this
        if not mower:
            for _ in range(self._rows):
                print(("+" + "- " * side) * self._cols + "+")
            for _ in range(side-1):
                print(("|" + "  " * side) * self._cols + "|")
        print(("+" + "- " * side) * self._cols + "+")
