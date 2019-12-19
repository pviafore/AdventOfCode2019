from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from math import ceil
from typing import Dict, List, Tuple

from common.input_handling import get_input

@dataclass(order=True)
class Chemical:
    num: int
    symbol: str


def to_chemical(text: str) -> Chemical:
    num, symbol = text.split(' ')
    return Chemical(int(num), symbol)


Reactions = Dict[str, Tuple[int, List[Chemical]]]
def to_reaction(text: str) -> Tuple[str, Tuple[int, List[Chemical]]]:
    ingredients_list, chemical = text.split(' => ')
    ingredients = ingredients_list.split(', ')
    chem = to_chemical(chemical)
    return (chem.symbol, (chem.num, [to_chemical(i) for i in ingredients]))


def get_reactions() -> Reactions:
    return dict(get_input("input/input14.txt", to_reaction))


def get_number_of_ore(reactions: Reactions, produced: int = 1) -> int:
    surplus: Counter = Counter({})
    return get_costs(reactions, Chemical(produced, "FUEL"), surplus)["ORE"]

def get_costs(reactions: Reactions, chemical: Chemical, surplus: Counter) -> Counter:
    if chemical.symbol == "ORE":
        return Counter({chemical.symbol: chemical.num})
    num_produced, ingredients_needed = deepcopy(reactions[chemical.symbol])
    if chemical.symbol in surplus:
        if chemical.num > surplus[chemical.symbol]:
            chemical.num -= surplus[chemical.symbol]
            del surplus[chemical.symbol]
        else:
            surplus[chemical.symbol] -= chemical.num
            if surplus[chemical.symbol] == 0:
                del surplus[chemical.symbol]
            return Counter({})

    if chemical.num > num_produced:
        for ingredient in ingredients_needed:
            ingredient.num *= ceil(chemical.num / num_produced)
        num_produced *= ceil(chemical.num / num_produced)
    costs: Counter = Counter({})
    for ingredient in ingredients_needed:
        costs += get_costs(reactions, ingredient, surplus)
    if num_produced > chemical.num:
        surplus[chemical.symbol] += (num_produced - chemical.num)
    return costs

def find_number_of_fuel(reactions: Reactions) -> int:
    ore_stockpile = 1_000_000_000_000
    ore_per_one_fuel = get_number_of_ore(reactions)

    minimum_fuel = ore_stockpile // ore_per_one_fuel
    maximum_fuel = minimum_fuel * 2
    while get_number_of_ore(reactions, maximum_fuel) < ore_stockpile:
        maximum_fuel += minimum_fuel

    return binary_search_fuel(minimum_fuel, maximum_fuel, reactions)

def binary_search_fuel(min_fuel: int, max_fuel: int, reactions: Reactions) -> int:
    if min_fuel >= max_fuel:
        return min_fuel
    target = 1_000_000_000_000
    average = (min_fuel + max_fuel) // 2 + 1
    if get_number_of_ore(reactions, average) >= target:
        return binary_search_fuel(min_fuel, average - 1, reactions)
    return binary_search_fuel(average, max_fuel, reactions)

REACTIONS = get_reactions()
if __name__ == "__main__":
    print(get_number_of_ore(REACTIONS))
    print(find_number_of_fuel(REACTIONS))
