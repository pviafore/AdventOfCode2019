from dataclasses import dataclass
from typing import Dict, List

@dataclass(frozen=True, order=True)
class Point:
    x: int # pylint: disable=invalid-name
    y: int # pylint: disable=invalid-name

    def to_right(self) -> 'Point':
        return Point(self.x + 1, self.y)

    def to_left(self) -> 'Point':
        return Point(self.x - 1, self.y)

    def to_above(self) -> 'Point':
        return Point(self.x, self.y + 1)

    def to_below(self) -> 'Point':
        return Point(self.x, self.y - 1)

ORIGIN = Point(0, 0)

def get_manhattan_distance(point1: Point, point2: Point) -> int:
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)

class TextGrid:
    def __init__(self, lines: List[str]):
        enumerated_lines = enumerate(enumerate(column) for column in lines)
        self._grid: Dict[Point, str] = {}
        for y_pos, enumerated_x in enumerated_lines:
            for x_pos, symbol in enumerated_x:
                self._grid[Point(x_pos, y_pos)] = symbol

    def get_all_points(self) -> Dict[Point, str]:
        return dict(self._grid)

    def get_all_points_matching_symbol(self, symbol: str) -> List[Point]:
        return [p for p, sym in self._grid.items() if sym == symbol]

    def set(self, point: Point, symbol: str):
        self._grid[point] = symbol

def get_slope(point1: Point, point2: Point) -> float:
    if point2.x == point1.x:
        return float("-inf") if point1.y > point2.y else float("inf")
    return (point2.y - point1.y) / (point2.x - point1.x)
