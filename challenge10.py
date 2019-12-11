from itertools import cycle
from typing import Dict, Generator, List, Tuple

from common.cartesian import get_manhattan_distance, get_slope, Point, TextGrid
from common.input_handling import get_input

ASTEROID = "#"
SlopeMapping = Dict[Tuple[bool, float], float]

def get_asteroids() -> TextGrid:
    asteroids = get_input("input/input10.txt")
    return TextGrid(asteroids)

def get_asteroids_seen(point: Point, asteroids: List[Point]) -> Tuple[Point, SlopeMapping]:
    mapping = get_slope_mapping(point, asteroids)
    return point, mapping

def get_slope_mapping(point: Point, asteroids: List[Point]) -> SlopeMapping:
    slope_mapping: SlopeMapping = {}
    for asteroid in asteroids:
        if point == asteroid:
            continue
        slope = get_slope(point, asteroid)
        distance = get_manhattan_distance(point, asteroid)
        slope_mapping[(point.x <= asteroid.x, slope)] = (
            min(slope_mapping.get((point.x <= asteroid.x, slope), 2**32), distance))
    return slope_mapping


def get_number_of_asteroids_seen_from_best_station(asteroid_grid: TextGrid) -> int:
    asteroids = asteroid_grid.get_all_points_matching_symbol(ASTEROID)
    return max(len(get_asteroids_seen(p, asteroids)[1]) for p in asteroids)

def get_200th_asteroid_destroyed(asteroid_grid: TextGrid) -> int:
    asteroids = asteroid_grid.get_all_points_matching_symbol(ASTEROID)
    point, mapping = max((get_asteroids_seen(p, asteroids) for p in asteroids),
                         key=lambda x: len(x[1]))
    order_of_slopes = get_order_of_slopes(mapping)
    for count, target in enumerate(fire_lasers(point, asteroids, order_of_slopes), start=1):
        if count == 200:
            return target.x*100 + target.y
    raise RuntimeError("Should never get here")

def fire_lasers(point: Point, asteroids: List[Point],
                order_of_slopes: List[Tuple[bool, float]]) -> Generator[Point, None, None]:
    for is_left, slope in cycle(order_of_slopes):
        targets = [a for a in asteroids
                   if point != a and get_slope(point, a) == slope and is_left == (point.x <= a.x)]
        target = min(targets, key=lambda a: get_manhattan_distance(point, a))
        asteroids.remove(target)
        yield target
    raise RuntimeError("Should never get here")


def get_order_of_slopes(mapping: SlopeMapping) -> List[Tuple[bool, float]]:
    angles = sorted(((is_left, angle) for is_left, angle in mapping if is_left))
    angles += sorted(((is_left, angle) for is_left, angle in mapping if not is_left))
    return angles

ASTEROIDS = get_asteroids()
if __name__ == "__main__":
    print(get_number_of_asteroids_seen_from_best_station(ASTEROIDS))
    print(get_200th_asteroid_destroyed(ASTEROIDS))
