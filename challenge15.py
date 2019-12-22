from collections import defaultdict
from enum import Enum, unique
from typing import List, Optional, Tuple

from common.cartesian import draw, get_orthogonal_points, Point
from common.input_handling import get_input
from common.intcode_computer import Computer

@unique
class TileType(Enum):
    WALL = 0
    EXPLORED = 1
    OXYGEN_STATION = 2
    EMPTY = 3


    def __str__(self):
        return '#.O '[int(self.value)]

class Map:

    def __init__(self):
        self.points: defaultdict = defaultdict(lambda: TileType.EMPTY)
        self.oxygen_station: Optional[Point] = None

    def explore(self, location: Point, tile_type: TileType):
        self.points[location] = tile_type
        if tile_type == TileType.OXYGEN_STATION:
            self.oxygen_station = location

    def is_explored(self, location: Point) -> bool:
        return location in self.points and self.points[location] != TileType.EMPTY

    def draw(self):
        draw(self.points, str)

    def is_oxygen_station(self, point: Point) -> bool:
        return self.oxygen_station == point

    def is_traversable(self, point: Point) -> bool:
        return self.points[point] in (TileType.EXPLORED, TileType.OXYGEN_STATION)

class Robot:

    def __init__(self):
        self.location = Point(0, 0)
        self.map = Map()
        self.map.explore(self.location, TileType.EXPLORED)
        self.next_move = Point(0, 0)
        self.unexplored = [(self.location, p) for p in get_orthogonal_points(self.location)]
        self.path: List[Point] = []
        self.is_backtracking = False

    def is_done_exploring(self) -> bool:
        return self.unexplored == []

    def get_movement_command(self) -> int:
        explored, self.next_move = self.unexplored[-1]

        if explored != self.location and not self.location.is_adjacent_to(self.next_move):
            self.next_move = self.path.pop()
            self.is_backtracking = True
        else:
            self.unexplored.pop()
            self.is_backtracking = False

        if self.next_move.y > self.location.y:
            return 1
        if self.next_move.y < self.location.y:
            return 2
        if self.next_move.x < self.location.x:
            return 3
        if self.next_move.x > self.location.x:
            return 4
        raise RuntimeError(f"Invalid Point {self.next_move}")

    def learn_map(self, value: int):
        self.map.explore(self.next_move, TileType(value))
        if TileType(value) != TileType.WALL:
            if not self.is_backtracking:
                self.path.append(self.location)
            self.location = self.next_move
        if TileType(value) == TileType.OXYGEN_STATION:
            print("OXYGEN", self.location)
            self.map.draw()
        next_points = [(self.location, p) for p in get_orthogonal_points(self.location) if
                       (self.location, p) not in self.unexplored]
        self.unexplored = [p for p in self.unexplored + next_points
                           if not self.map.is_explored(p[1])]

    def get_distance_to_oxygen_station(self) -> int:
        seen = set([])
        points: List[Tuple[int, Point]] = [(0, Point(0, 0))]
        while points:
            distance, point = points.pop(0)
            if self.map.is_oxygen_station(point):
                return distance
            seen.add(point)
            adjacent_points = get_orthogonal_points(point)
            valid_points = [(distance + 1, p) for p in adjacent_points if
                            self.map.is_traversable(p) and p not in seen]
            points += valid_points
        raise RuntimeError("This should be unreachable")

    def calculate_distance_for_oxygen_to_progpagate(self) -> int:
        seen = set([])
        points: List[Tuple[int, Point]] = [(0, self.map.oxygen_station)]
        while points:
            distance, point = points.pop(0)
            seen.add(point)
            adjacent_points = get_orthogonal_points(point)
            valid_points = [(distance + 1, p) for p in adjacent_points if
                            self.map.is_traversable(p) and p not in seen]
            points += valid_points
        return distance




def load_instructions() -> List[int]:
    return get_input("input/input15.txt", int, delimiter=",")

def run_program() -> Robot:
    computer = Computer(load_instructions())
    robot = Robot()
    computer.input_function = robot.get_movement_command
    computer.output_function = robot.learn_map
    computer.halt_function = robot.is_done_exploring
    computer.run_loop()
    return robot

if __name__ == "__main__":
    print(run_program().get_distance_to_oxygen_station())
    print(run_program().calculate_distance_for_oxygen_to_progpagate())
