from typing import Callable, Dict, List, Set

from common.cartesian import get_manhattan_distance, ORIGIN, Point
from common.input_handling import get_input

DIRECTION_MAPPING: Dict[str, Callable[[Point], Point]] = {
    "U": Point.to_above,
    "D": Point.to_below,
    "L": Point.to_left,
    "R": Point.to_right
}

Wire = List[Point]

def get_wire_points(wire_string: str) -> Wire:
    path = wire_string.split(",")

    points = [ORIGIN]
    for segment in path:
        direction, length = segment[0], int(segment[1:])
        for _ in range(length):
            next_point_func = DIRECTION_MAPPING[direction]
            points.append(next_point_func(points[-1]))
    return points

def get_distance_to_closest_intersection(wires: List[Wire]) -> int:
    intersections: Set[Point] = set(wires[0]) & set(wires[1]) - set([ORIGIN])
    closest_intersection = min(intersections, key=lambda i: get_manhattan_distance(i, ORIGIN))
    return get_manhattan_distance(closest_intersection, ORIGIN)

def get_minimal_timing_delay(wires: List[Wire]) -> int:
    intersections: Set[Point] = set(wires[0]) & set(wires[1]) - set([ORIGIN])
    wire1 = list(enumerate(wires[0]))
    wire2 = list(enumerate(wires[1]))

    shortest_distance = 2**256
    for intersection in intersections:
        wire1_distance = next(distance for distance, point in wire1 if point == intersection)
        wire2_distance = next(distance for distance, point in wire2 if point == intersection)
        shortest_distance = min(shortest_distance, wire1_distance + wire2_distance)
    return shortest_distance


WIRES = get_input("input/input3.txt", get_wire_points)
if __name__ == "__main__":
    print(get_distance_to_closest_intersection(WIRES))
    print(get_minimal_timing_delay(WIRES))
