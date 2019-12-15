import re

from dataclasses import dataclass
from typing import List

from common.input_handling import get_input

@dataclass
class XYZ:
    x: int # pylint: disable=invalid-name
    y: int # pylint: disable=invalid-name
    z: int # pylint: disable=invalid-name

    def get_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

def get_velocity_change(value1: int, value2: int) -> int:
    if value1 < value2:
        return 1
    if value1 > value2:
        return -1
    return 0


class Moon:
    def __init__(self, x, y, z):
        self.position = XYZ(x, y, z)
        self.velocity = XYZ(0, 0, 0)

    def __str__(self) -> str:
        return f"{self.position} {self.velocity}"

    def adjust_gravity(self, moons: List["Moon"]):
        for moon in moons:
            self.velocity.x += get_velocity_change(self.position.x, moon.position.x)
            self.velocity.y += get_velocity_change(self.position.y, moon.position.y)
            self.velocity.z += get_velocity_change(self.position.z, moon.position.z)

    def move(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        self.position.z += self.velocity.z

    def get_total_energy(self) -> int:
        return self.position.get_energy() * self.velocity.get_energy()

def to_moon(text: str) -> Moon:
    matches = re.match(r'<x=(-?\d*), y=(-?\d*), z=(-?\d*)>', text)
    if matches is None:
        raise RuntimeError("Invalid input")
    return Moon(int(matches[1]), int(matches[2]), int(matches[3]))

def get_moons() -> List[Moon]:
    return get_input("input/input12.txt", to_moon)

def run_simulation(ticks: int, moons: List[Moon]) -> int:
    for _ in range(ticks):
        for moon in moons:
            moon.adjust_gravity(moons)
        for moon in moons:
            moon.move()
    return sum(m.get_total_energy() for m in moons)

MOONS = get_moons()
if __name__ == "__main__":
    print(run_simulation(1000, MOONS))
