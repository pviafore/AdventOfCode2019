from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

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
