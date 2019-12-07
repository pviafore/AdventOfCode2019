from typing import Dict, Generator, List
from common.input_handling import get_input

Orbits = Dict[str, str]

def to_orbit(text: str) -> List[str]:
    return text.split(")")[::-1]

def get_orbits() -> Orbits:
    return dict(get_input("input/input6.txt", to_orbit))

def get_total_orbits(orbits: Orbits) -> int:
    return sum(_get_orbit_checksum(orbits, body) for body in orbits)

def _get_orbit_checksum(orbits: Orbits, root: str) -> int:
    return 0 if root == "COM" else 1 + _get_orbit_checksum(orbits, orbits[root])

def get_transfer_distance(orbits: Orbits) -> int:
    your_orbit = orbits["YOU"]
    santas_orbit = orbits["SAN"]
    nodes = [(0, your_orbit)]
    nodes_seen = set([your_orbit])
    while True:
        distance, node = nodes.pop(0)
        if node == santas_orbit:
            return distance
        for next_node in _get_connecting_nodes(orbits, node):
            if next_node not in nodes_seen:
                nodes.append((distance + 1, next_node))
                nodes_seen.add(next_node)
    raise RuntimeError("It is not possible to get here")

def _get_connecting_nodes(orbits: Orbits, node: str) -> Generator[str, None, None]:
    if node in orbits:
        yield orbits[node]
    for orbiter, body in orbits.items():
        if body == node:
            yield orbiter

ORBITS = get_orbits()
if __name__ == "__main__":
    print(get_total_orbits(ORBITS))
    print(get_transfer_distance(ORBITS))
