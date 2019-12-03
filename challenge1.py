"""
Day 1
"""

from typing import List
from common.input_handling import get_input
def get_fuel(mass: int):
    return mass // 3 - 2

def get_total_fuel(masses: List[int]):
    return sum(get_fuel(mass) for mass in masses)

def get_total_additional_fuel(masses: List[int]):
    return sum(get_additional_fuel_consumption(mass) for mass in masses)

def get_additional_fuel_consumption(mass: int):
    additional_fuel = get_fuel(mass)
    if additional_fuel > 0:
        return additional_fuel + get_additional_fuel_consumption(additional_fuel)
    return 0


MASSES = get_input("input/input1.txt", int)
if __name__ == "__main__":
    print(get_total_fuel(MASSES))
    print(get_total_additional_fuel(MASSES))
